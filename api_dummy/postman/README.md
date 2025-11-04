# Colección Postman para Vhape Dummy API

Colección completa de Postman y environment para probar todos los escenarios de autenticación del API dummy de Vhape.

## Archivos

- **Vhape_Dummy_API.postman_collection.json** - Colección de pruebas completa con todos los endpoints
- **Vhape_Dummy_API.postman_environment.json** - Variables de environment con tokens y URL base

## Instrucciones de Importación

### Paso 1: Importar Colección

1. Abrir Postman
2. Clic en botón **Import** (arriba a la izquierda)
3. Clic en **Upload Files**
4. Seleccionar `Vhape_Dummy_API.postman_collection.json`
5. Clic en **Import**

### Paso 2: Importar Environment

1. Clic en botón **Import** nuevamente
2. Clic en **Upload Files**
3. Seleccionar `Vhape_Dummy_API.postman_environment.json`
4. Clic en **Import**

### Paso 3: Seleccionar Environment

1. En la esquina superior derecha, clic en el dropdown de environment
2. Seleccionar **"Vhape Dummy API - Local"**

## Estructura de la Colección

La colección está organizada en 3 carpetas:

### 1. Health Check
- `GET /api/health` - Verificar que el servidor funciona

**Esperado:** Retorna `200 OK` sin autenticación

### 2. Users - Get Current User Profile
- `GET /api/users/me` (con token válido) → `200` (validate token)
- `GET /api/users/me` (con token inválido) → `401` (expect 401)
- `GET /api/users/me` (sin token) → `401` (expect 401)

**Esperado:** Retorna `200 OK` con token válido (validate token), `401 Unauthorized` con token inválido o sin token (expect 401)

### 3. Admin - Get All Users
- `GET /api/admin/users` (con token usuario) → `403` (access denied)
- `GET /api/admin/users` (con token admin) → `200` (access allowed)

**Esperado:** Retorna `403 Forbidden` con token de usuario (access denied), `200 OK` con token admin (access allowed)

## Variables de Environment

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `base_url` | `http://localhost:8000` | URL base del API |
| `valid_token` | `valid-token` | Token de usuario admin |
| `user_token` | `user-token` | Token de usuario regular |
| `invalid_token` | `invalid-token` | Token inválido para pruebas |
| `expired_token` | `expired-token` | Token expirado para pruebas |

## Ejecutar Pruebas

### Ejecutar Request Individual

1. Seleccionar un request de la colección
2. Clic en **Send**
3. Revisar la pestaña **Test Results** para ver los resultados de validación

### Ejecutar Colección Completa

1. Clic derecho en el nombre de la colección
2. Seleccionar **Run collection**
3. Clic en **Run Vhape Dummy API - Suite de Pruebas**
4. Revisar resultados de todas las pruebas

### Ejecutar con Collection Runner

1. Clic en **Collections** en la barra lateral
2. Clic en **Run** junto a la colección
3. Seleccionar qué requests ejecutar
4. Clic en **Run Vhape Dummy API**
5. Ver resumen de resultados

## Scripts de Prueba

Cada request incluye scripts automatizados que validan:

- ✅ **Códigos de estado** - Verifica códigos HTTP correctos
- ✅ **Estructura de respuesta** - Verifica propiedades JSON esperadas
- ✅ **Mensajes de error** - Valida mensajes de detalle de error
- ✅ **Validación de datos** - Asegura que los datos de respuesta coincidan con las expectativas

## Prueba de DSL Keywords

La colección incluye endpoints específicos para probar DSL keywords:

### `validate token`
- **Endpoint:** `GET /api/users/me`
- **Uso:** Token válido en header Authorization
- **Esperado:** `200 OK` con perfil de usuario

### `expect 401`
- **Endpoint:** `GET /api/users/me`
- **Uso:** Sin token o con token inválido
- **Esperado:** `401 Unauthorized`

### `access denied`
- **Endpoint:** `GET /api/admin/users`
- **Uso:** Token de usuario en endpoint admin
- **Esperado:** `403 Forbidden`

### `access allowed`
- **Endpoint:** `GET /api/admin/users`
- **Uso:** Token admin en endpoint admin
- **Esperado:** `200 OK`

## Referencia de Códigos de Estado

| Código | Significado | Cuándo Ocurre |
|--------|-------------|---------------|
| `200 OK` | Éxito | Token válido, acceso autorizado |
| `401 Unauthorized` | Autenticación fallida | Token inválido o faltante |
| `403 Forbidden` | Autorización fallida | Token válido pero sin permisos suficientes |

## Consejos

1. **Verificar Environment**: Siempre asegurar que "Vhape Dummy API - Local" esté seleccionado
2. **Servidor Corriendo**: Asegurar que el servidor API esté corriendo en `http://localhost:8000`
3. **Ver Resultados**: Clic en cualquier request y revisar la pestaña **Test Results**
4. **Modificar Variables**: Editar variables de environment si necesitas diferentes tokens o URLs
5. **Exportar Resultados**: Usar la función de exportar de Postman para guardar resultados de pruebas

## Solución de Problemas

### La colección no se importa
- Asegurar que estás usando Postman v9.0 o posterior
- Verificar que los archivos JSON sean válidos

### Las pruebas fallan
- Verificar que el servidor API esté corriendo: `./api_dummy/run.sh`
- Verificar que el environment esté seleccionado
- Verificar que `base_url` apunte al servidor correcto

### Las variables no funcionan
- Asegurar que el environment esté seleccionado en el dropdown
- Verificar que los nombres de variables coincidan exactamente (sensible a mayúsculas)
- Verificar que las variables estén habilitadas en el environment

## Próximos Pasos

Después de importar y ejecutar la colección:

1. ✅ Verificar que todas las pruebas pasen
2. ✅ Revisar estructuras de respuesta
3. ✅ Probar casos límite manualmente
4. ✅ Exportar resultados para documentación
5. ✅ Compartir colección con miembros del equipo
