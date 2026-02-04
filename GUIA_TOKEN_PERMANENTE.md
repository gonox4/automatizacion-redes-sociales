# Guía: Obtener Token Permanente de Facebook

Para que la automatización funcione sin que tengas que actualizar el token cada hora, necesitas crear una "App" en Facebook. Es un proceso de única vez.

## Paso 1: Crear una App en Meta Developers

1. Ve a [Tus Apps en Meta for Developers](https://developers.facebook.com/apps/).
2. Haz clic en el botón verde **Create App** (Crear App).
3. Selecciona **Other** (Otro) > **Next**.
4. Selecciona **Business** (Negocios) > **Next**.
5. Rellena los datos:
   - **App Name**: `AutomatizacionBot` (o lo que quieras).
   - **App Contact Email**: Tu email.
   - **Business Account**: Selecciona tu cuenta de negocio si tienes una, o déjalo sin seleccionar.
6. Haz clic en **Create App** (te pedirá tu contraseña de FB).

## Paso 2: Obtener Credenciales de la App

Una vez creada la App, estarás en el panel de control (Dashboard).

1. En el menú lateral izquierdo, ve a **App settings** (Configuración) -> **Basic** (Básica).
2. Aquí verás:
   - **App ID**: Un número largo.
   - **App Secret**: Un campo oculto. Haz clic en "Show" (Mostrar).
3. **Copia estos dos valores** y pégalos en tu archivo `.env` añadiendo estas líneas al final:

```env
FB_APP_ID=copea_aqui_tu_app_id
FB_APP_SECRET=copea_aqui_tu_app_secret
```

## Paso 3: Generar el Token Base con TU App

Ahora volvemos al Graph Explorer, pero usaremos TU App en lugar de la genérica.

1. Ve al [Graph API Explorer](https://developers.facebook.com/tools/explorer/).
2. En **Meta App** (a la derecha), selecciona **Tu Nueva App** (AutomatizacionBot) en el desplegable.
3. En **User or Page**, selecciona "User Token".
4. En **Permissions**, añade de nuevo (si no están):
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `instagram_basic`
   - `instagram_content_publish`
5. Haz clic en **Generate Access Token**.
6. Autoriza los permisos nuevamente (Continuar como tú, seleccionar páginas, aceptar todo).
7. **Copia el Token que se ha generado**.

## Paso 4: Ejecutar el Script de Conversión

Este token que acabas de copiar dura solo 1 hora, pero sirve de "semilla" para el permanente.

1. Abre tu `.env` y pega ese token corto en:
   ```env
   FB_SHORT_TOKEN=pega_aqui_el_token_corto_del_explorer
   ```
2. Guarda el archivo `.env`.
3. Ejecuta este script en la terminal de VS Code:
   ```bash
   python get_long_lived_token.py
   ```

## Resultado

El script te mostrará un **NUEVO TOKEN LARGO** (empieza igual pero es mucho más largo). 
El script intentará actualizar tu archivo `.env` automáticamente, o te pedirá que lo copies y pegues en `FB_PAGE_ACCESS_TOKEN`.

¡Ese nuevo token durará indefinidamente! (o al menos 60 días renovables automáticamente).
