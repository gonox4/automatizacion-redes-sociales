# Guía Paso a Paso: Generar Token de Facebook e Instagram

Como no puedo iniciar sesión en tu cuenta por seguridad (autenticación de dos pasos, contraseñas), aquí tienes la guía exacta para hacerlo tú mismo en 2 minutos.

## Paso 1: Abrir Graph API Explorer
1. Ve a esta URL en tu navegador: [https://developers.facebook.com/tools/explorer/](https://developers.facebook.com/tools/explorer/)
2. Asegúrate de iniciar sesión con tu cuenta de Facebook (Dorian Bale).

## Paso 2: Configurar la App
En el panel de la derecha ("Meta App"):
1. Si tienes una App creada, selecciónala.
2. Si no, o si prefieres evitar problemas, selecciona **Graph API Explorer** en el desplegable "Meta App".

## Paso 3: Permisos (La parte CLAVE)
En la sección "Permissions" (Permisos), busca y agrega uno por uno estos permisos (usa el buscador que aparece al dar clic):

**Para Facebook:**
*   `pages_manage_posts` (Para publicar)
*   `pages_read_engagement` (Para leer datos)

**Para Instagram:**
*   `instagram_basic`
*   `instagraen m_content_publish`

## Paso 4: Generar Token y Seleccionar Página
1. Haz clic en el botón azul **Generate Access Token**.
2. **¡IMPORTANTE!** Te saldrá una ventana emergente de Facebook.
    *   Si te pregunta "¿Quieres continuar como Dorian?", di que **SÍ**.
    *   **PANTALLA "Qué páginas quieres usar"**: Aquí es donde falló antes. Marca la casilla de **[X] La Cueva del Eco**. Si tienes opción "Seleccionar todas", mejor.
    *   **PANTALLA "Permisos"**: Dale a "Permitir" o "Guardar" a todo.

## Paso 5: Obtener el ID de la Página y Token
Una vez cerrada la ventana emergente, verás un "Access Token" largo arriba.

1. Copia y pega temporalmente ese token en el campo `FB_PAGE_ACCESS_TOKEN` de tu archivo `.env`. (Borra el anterior).
2. Para encontrar el ID correcto de la página, en la barra superior de la herramienta (donde dice `GET` y `v19.0`), escribe:
   `me/accounts`
   Y dale al botón azul **Submit**.
3. En la respuesta (el JSON de abajo), busca "La Cueva del Eco". Verás algo como:
   ```json
   {
     "name": "La Cueva del Eco",
     "id": "123456789...",  <-- ESTE ES TU FB_PAGE_ID
     "access_token": "..."
   }
   ```
4. Copia ese ID numérico y ponlo en `FB_PAGE_ID` en tu `.env`.

## Paso 6: Obtener el ID de Instagram
En la misma barra de arriba, borra lo anterior y pon:
`me/accounts?fields=instagram_business_account`
Dale a **Submit**.

Busca tu página. Debería salir algo como:
```json
"instagram_business_account": {
    "id": "987654..." <-- ESTE ES TU IG_ACCOUNT_ID
}
```
Si esto no sale, es que tu Instagram no está conectado a la Fan Page (Avísame si pasa esto).

---
**Resumen para el archivo .env:**
1. Copia el Token generado.
2. Copia el ID de la Página.
3. Copia el ID de Instagram.
