# Vhape Dummy API - HU2

API dummy simple para probar los DSL keywords del framework Vhape BDD.

## Propósito

API minimalista que permite probar los DSL keywords:
- `validate token` - Validar token de autenticación
- `expect 401` - Esperar respuesta 401 (probar con `/validate-token` sin token o token inválido)
- `access denied` - Esperar respuesta 403 (acceso denegado)

## Características

- **3 endpoints esenciales** para probar los DSL keywords
- **Documentación automática** en `/docs` (FastAPI)
- **Tokens simples** para testing

## Ejecutar el API

### Prerrequisitos

```bash
# Activar entorno virtual
source .venv/bin/activate

# Instalar dependencias (si no están instaladas)
pip install -r requirements.txt
```

### Método 1: Script Bash (Recomendado)

```bash
./api_dummy/run.sh
```

### Método 2: Python

```bash
python api_dummy/run.py
```

### Método 3: Uvicorn directo

```bash
python -m uvicorn api_dummy.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints

### Health Check

```
GET /api/health
```

Endpoint público para verificar que el servidor está funcionando.

**Respuesta:** `200 OK`
```json
{"status": "healthy"}
```

### Get Current User Profile

```
GET /api/users/me
Authorization: Bearer <token>
```

**DSL keywords:** `validate token` / `expect 401`

- **Token válido:** `valid-token` → `200 OK` (validate token)
- **Token inválido:** `invalid-token` → `401 Unauthorized` (expect 401)
- **Sin token:** → `401 Unauthorized` (expect 401)

**Ejemplo con token válido:**
```bash
curl -H "Authorization: Bearer valid-token" http://localhost:8000/api/users/me
```

**Respuesta:** `200 OK`
```json
{
  "user_id": "user1",
  "role": "admin",
  "message": "User profile retrieved successfully"
}
```

### Get All Users (Admin Only)

```
GET /api/admin/users
Authorization: Bearer <token>
```

**DSL keyword:** `access denied`

- **Token admin:** `valid-token` → `200 OK` (access allowed)
- **Token usuario:** `user-token` → `403 Forbidden` (access denied)
- **Sin token:** → `401 Unauthorized`

**Ejemplo con token de usuario (espera 403):**
```bash
curl -H "Authorization: Bearer user-token" http://localhost:8000/api/admin/users
```

**Respuesta:** `403 Forbidden`
```json
{
  "detail": "Access denied"
}
```

**Ejemplo con token admin (espera 200):**
```bash
curl -H "Authorization: Bearer valid-token" http://localhost:8000/api/admin/users
```

**Respuesta:** `200 OK`
```json
{
  "users": [
    {"id": "user1", "role": "admin"},
    {"id": "user2", "role": "user"}
  ],
  "message": "Users list retrieved successfully",
  "accessed_by": "user1"
}
```

## Tokens para Testing

### Tokens Válidos

| Token | Rol | Uso |
|-------|-----|-----|
| `valid-token` | admin | Probar acceso admin (200) |
| `user-token` | user | Probar acceso denegado (403) |

### Tokens Inválidos

| Token | Resultado |
|-------|-----------|
| `invalid-token` | 401 Unauthorized |
| `expired-token` | 401 Unauthorized |
| (sin token) | 401 Unauthorized |

## Ejemplos de Uso

### Probar "validate token"

```bash
# Token válido (debe retornar 200)
curl -H "Authorization: Bearer valid-token" http://localhost:8000/api/users/me

# Token inválido (debe retornar 401)
curl -H "Authorization: Bearer invalid-token" http://localhost:8000/api/users/me

# Sin token (debe retornar 401)
curl http://localhost:8000/api/users/me
```

### Probar "expect 401"

```bash
# Sin token en /api/users/me (debe retornar 401)
curl http://localhost:8000/api/users/me

# Token inválido en /api/users/me (debe retornar 401)
curl -H "Authorization: Bearer invalid-token" http://localhost:8000/api/users/me
```

### Probar "access denied"

```bash
# Token de usuario en endpoint admin (debe retornar 403)
curl -H "Authorization: Bearer user-token" http://localhost:8000/api/admin/users

# Token admin (debe retornar 200)
curl -H "Authorization: Bearer valid-token" http://localhost:8000/api/admin/users
```

## Documentación Interactiva

Una vez que el servidor esté corriendo:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Mapeo DSL Keywords

| DSL Keyword | Endpoint | Caso de Prueba |
|------------|----------|----------------|
| `validate token` | `/api/users/me` | Token válido → 200 |
| `expect 401` | `/api/users/me` | Sin token o token inválido → 401 |
| `access denied` | `/api/admin/users` | Token usuario en endpoint admin → 403 |
| `access allowed` | `/api/admin/users` | Token admin en endpoint admin → 200 |

## Códigos de Estado

- `200 OK` - Token válido y acceso autorizado
- `401 Unauthorized` - Token inválido o faltante
- `403 Forbidden` - Token válido pero sin permisos

## Desarrollo

Este API es parte del proyecto Vhape MVP y se usa internamente para pruebas BDD. No está diseñado para uso en producción.
