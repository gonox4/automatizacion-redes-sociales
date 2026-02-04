import os
import glob
import logging
import json
import datetime
from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import main  # Importamos tu script existente
import threading
from google import genai
from google.genai import types

# Configuración de logs para la API
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Servir archivos estáticos (Frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Estado Global de Configuración (Persistencia simple en JSON)
CONFIG_FILE = "node_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    # Default config
    return {
        "timer_enabled": True,
        "sheet_enabled": True,
        "ai_enabled": False, # Disabled by default for stability
        "fb_enabled": True,
        "ig_enabled": True
    }

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

@app.get("/")
def read_root():
    return JSONResponse(content={"message": "Social Media Bot API is running"})

@app.get("/config")
def get_config():
    """Devuelve la configuración de nodos activos."""
    return load_config()

@app.post("/config")
def update_config(config: dict = Body(...)):
    """Actualiza la configuración de nodos."""
    current = load_config()
    current.update(config)
    save_config(current)
    return current

@app.get("/stats")
def get_stats():
    """Devuelve estadísticas y tiempo restante."""
    try:
        client = main.get_google_sheets_client()
        sheet = client.open_by_key(main.GOOGLE_SHEETS_ID).sheet1
        records = sheet.get_all_records()
        
        pending = [r for r in records if r.get('ESTADO') == 'PENDIENTE']
        published = [r for r in records if r.get('ESTADO') == 'PUBLICADO' or r.get('ESTADO') == 'PUBLICADO_SOLO_FB']
        
        # Calcular Next Run (10:00 AM Mañana o Hoy si es antes)
        now = datetime.datetime.now()
        target_today = now.replace(hour=10, minute=0, second=0, microsecond=0)
        
        if now < target_today:
            next_run = target_today
        else:
            next_run = target_today + datetime.timedelta(days=1)
            
        time_remaining = (next_run - now).total_seconds()
        
        next_post = None
        if pending:
            first = pending[0]
            next_post = {
                "id": first.get("ID"),
                "prompt": first.get("PROMPT_IMAGEN"),
                "caption": first.get("TEXTO_POST"),
                "time": first.get("HORA_PUBLICACION")
            }
        
        last_image = None
        if os.path.exists("static/generated/last_gen.png"):
            # Generar un timestamp para evitar cache del navegador
            ts = int(datetime.datetime.now().timestamp())
            last_image = f"/static/generated/last_gen.png?t={ts}"
        
        return {
            "pending": len(pending),
            "published": len(published),
            "total": len(records),
            "next_run_ts": next_run.timestamp(),
            "seconds_remaining": int(time_remaining),
            "next_post": next_post,
            "last_image": last_image
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return {"error": str(e)}

@app.get("/posts")
def get_posts():
    """Obtiene los posts del Google Sheet."""
    try:
        client = main.get_google_sheets_client()
        sheet = client.open_by_key(main.GOOGLE_SHEETS_ID).sheet1
        records = sheet.get_all_records()
        
        # Procesar datos para el frontend
        processed = []
        for i, r in enumerate(records):
            processed.append({
                "id": r.get("ID"),
                "prompt": r.get("PROMPT_IMAGEN"),
                "caption": r.get("TEXTO_POST"),
                "status": r.get("ESTADO"),
                "time": r.get("HORA_PUBLICACION"),
                "row": i + 2
            })
        return processed
    except Exception as e:
        logger.error(f"Error reading sheets: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs")
def get_logs():
    """Lee las últimas líneas del log."""
    log_file = "bot_log.txt"
    if not os.path.exists(log_file):
        return {"logs": ["No logs found."]}
    
    try:
        with open(log_file, "r") as f:
            lines = f.readlines()
        return {"logs": [l.strip() for l in lines[-50:]]} # Últimas 50 líneas
    except Exception as e:
        return {"logs": [f"Error reading logs: {e}"]}

@app.post("/run-now")
def run_listing():
    """Ejecuta el bot inmediatamente en un hilo separado."""
    def run_bot_thread():
        logger.info("Starting manual execution...")
        config = load_config()
        # Aquí podríamos inyectar la config en main si main soportara argumentos
        # Por ahora main corre todo, pero podríamos modificar main para chequear config.
        # Para simplificar, asumimos que run-now fuerza todo, o podríamos parchear main.
        try:
            main.main()
        except Exception as e:
            logger.error(f"Manual execution failed: {e}")
            
    thread = threading.Thread(target=run_bot_thread)
    thread.start()
    return {"status": "Execution started"}

# --- AI CHAT COMMANDER ---
GEMINI_CLIENT = genai.Client(api_key=main.GEMINI_API_KEY)

class ChatMessage(BaseModel):
    message: str

@app.post("/chat")
def chat_commander(msg: ChatMessage):
    """Interfaz de chat con IA para controlar el sistema."""
    config = load_config()
    if not config.get('ai_enabled', False):
        return {
            "reply": "⚠️ El sistema de IA está desactivado actualmente para ahorrar recursos. Puedes reactivarlo en la configuración si tienes una API Key válida.",
            "actions": []
        }

    try:
        # Definir las herramientas (funciones) que la IA puede llamar
        tools = [
            {
                "function_declarations": [
                    {
                        "name": "toggle_node",
                        "description": "Activa o desactiva un nodo/servicio específico (timer, sheet, ai, fb, ig).",
                        "parameters": {
                            "type": "OBJECT",
                            "properties": {
                                "node_id": {"type": "STRING", "description": "ID del nodo (timer, sheet, ai, fb, ig)"},
                                "enabled": {"type": "BOOLEAN", "description": "True para activar, False para desactivar"}
                            },
                            "required": ["node_id", "enabled"]
                        }
                    },
                    {
                        "name": "get_system_stats",
                        "description": "Obtiene estadísticas actuales del sistema: posts pendientes, publicados, etc.",
                    },
                    {
                        "name": "run_manual_bot",
                        "description": "Inicia la ejecución manual del bot de redes sociales ahora mismo.",
                    }
                ]
            }
        ]

        system_instruction = (
            "Eres el Comandante de IA de un sistema de automatización de redes sociales. "
            "Tu objetivo es ayudar al usuario a gestionar sus nodos (Planificador, Sheets, IA, Facebook, Instagram) "
            "y responder dudas. Puedes activar/desactivar servicios, dar estadísticas o lanzar el bot. "
            "Responde de forma concisa, profesional y con un toque futurista. Usa emojis de tecnología. "
            "Si realizas una acción, confírmala."
        )

        response = GEMINI_CLIENT.models.generate_content(
            model='gemini-2.5-flash',
            contents=msg.message,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=tools
            )
        )

        # Procesar llamadas a funciones si existen
        actions = []
        final_text = ""
        
        # Recorrer partes de la respuesta
        for part in response.candidates[0].content.parts:
            if part.text:
                final_text += part.text
            if part.call:
                call = part.call
                if call.name == "toggle_node":
                    nid = call.args["node_id"]
                    val = call.args["enabled"]
                    update_config({f"{nid}_enabled": val})
                    actions.append(f"Nodo {nid} {'activado' if val else 'desactivado'}")
                elif call.name == "get_system_stats":
                    stats_data = get_stats()
                    actions.append(f"Estadísticas obtenidas: {stats_data.get('pending')} pendientes.")
                    # Generar respuesta de seguimiento con los datos
                    follow_up = GEMINI_CLIENT.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=f"El sistema tiene estos datos: {stats_data}. Resúmelos para el usuario."
                    )
                    final_text += "\n" + follow_up.text
                elif call.name == "run_manual_bot":
                    run_listing()
                    actions.append("Ejecución manual iniciada")
                    final_text += "\n🚀 ¡Entendido! He iniciado el proceso de publicación manual por ti."

        return {
            "reply": final_text if final_text else "He procesado tu comando, Comandante.",
            "actions": actions
        }

    except Exception as e:
        logger.error(f"Chat error: {e}")
        return {"reply": f"Lo siento, Comandante. Mi núcleo de procesamiento ha fallado: {str(e)}", "actions": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
