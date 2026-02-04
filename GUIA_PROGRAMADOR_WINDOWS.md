# Guía: Programar Publicaciones con Windows

Como hemos configurado el bot para que publique "un post cada vez", ahora debemos decirle a Windows que ejecute este script automáticamente (por ejemplo, cada 24 horas).

## Pasos para Configurar el Programador de Tareas

1.  **Abrir el Programador**:
    *   Pulsa la tecla **Windows**, escribe `Programador de tareas` y ábrelo.

2.  **Crear Tarea**:
    *   En el panel derecho, pulsa en **"Crear tarea básica..."**.
    *   Ponle un nombre: `Bot Redes Sociales`.
    *   Descripción: `Publica un post automáticamente`.

3.  **Desencadenador (Cuándo ejecutar)**:
    *   Elige **"Diariamente"**.
    *   Establece la hora a la que quieres que se publique (ej: 10:00 AM).
    *   Repetir cada: **1 día**.

4.  **Acción (Qué hacer)**:
    *   Elige **"Iniciar un programa"**.
    *   **Programa o script**: `python` (o la ruta completa a tu `python.exe` si no funciona, que suele ser `C:\Windows\py.exe` o similar).
    *   **Agregar argumentos (opcional)**: Escribe el nombre de tu archivo entre comillas: `"main.py"`.
    *   **Iniciar en (opcional)**: **IMPORTANTE**. Copia y pega la ruta de la carpeta donde está tu script: `c:\Users\Usuario\.gemini\antigravity\scratch\automatizacion-redes-sociales`.

5.  **Finalizar**:
    *   Dale a finalizar y verás tu tarea en la lista.

## Prueba

*   Haz clic derecho sobre tu nueva tarea en la lista y dale a **"Ejecutar"**.
*   Debería abrirse una ventana negra brevemente, publicar el post y cerrarse.
*   ¡Listo! Tu PC ahora es un servidor de automatización.

> [!NOTE]
> Tu PC debe estar encendido a la hora programada para que funcione.
