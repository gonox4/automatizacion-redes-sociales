# Guía de Despliegue en GitHub

Para que el bot funcione desde GitHub Actions (y no desde tu PC), necesitas configurar los "Secretos" (Secrets) en tu repositorio. GitHub necesita las claves para acceder a Facebook, Instagram y Gemini.

## 1. Configurar Secretos en GitHub

Ve a tu repositorio en GitHub -> **Settings** -> **Secrets and variables** -> **Actions** -> **New repository secret**.

Añade las siguientes claves (copia los valores de tu archivo `.env` y `credentials.json`):

| Nombre del Secreto | Valor a copiar |
|--------------------|----------------|
| `FB_PAGE_ACCESS_TOKEN` | El valor de `FB_PAGE_ACCESS_TOKEN` en `.env` |
| `FB_PAGE_ID` | El valor de `FB_PAGE_ID` en `.env` |
| `IG_ACCOUNT_ID` | El valor de `IG_ACCOUNT_ID` en `.env` |
| `GEMINI_API_KEY` | El valor de `GEMINI_API_KEY` en `.env` |
| `GOOGLE_SHEETS_ID` | El valor de `GOOGLE_SHEETS_ID` en `.env` |
| `GOOGLE_CREDENTIALS_JSON` | **Todo el contenido** del archivo `credentials.json` (ábrelo con bloc de notas y copia todo) |

> ⚠️ **IMPORTANTE**: Para `GOOGLE_CREDENTIALS_JSON`, asegúrate de copiar todo el contenido del archivo JSON, incluyendo las llaves `{` y `}`.

## 2. Desactivar la Tarea de Windows (Opcional pero recomendado)

Si vas a usar GitHub, deberías desactivar la tarea de Windows para evitar publicaciones duplicadas.

1. Abre "Programador de tareas" (Task Scheduler) en Windows.
2. Busca la tarea `SocialMediaBot`.
3. Clic derecho -> **Deshabilitar** (Disable) o **Eliminar** (Delete).

## 3. Verificar el Funcionamiento

Una vez subido el código a GitHub:
1. Ve a la pestaña **Actions** en tu repositorio.
2. Verás el flujo "Publicar Post Diario".
3. Puedes esperar a mañana a las 10:00 (hora programada) o probarlo manualmente haciendo clic en el flujo -> **Run workflow**.

---
**Nota sobre la hora**: El bot en GitHub está configurado para ejecutarse a las 09:00 UTC, que son las 10:00 AM en España (horario de invierno).
