# Vhape Dummy API - HU2

API dummy simple para probar los DSL keywords del framework Vhape BDD.

## Propósito

API minimalista que permite probar los DSL keywords:
- `validate token` - Validar token de autenticación
- `expect 401` - Esperar respuesta 401 (no autorizado)
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
GET /health
```

Endpoint público para verificar que el servidor está funcionando.

**Respuesta:** `200 OK`
```json
{"status": "healthy"}
```

### Validate Token

```
GET /validate-token
Authorization: Bearer <token>
```

**DSL keyword:** `validate token`

- **Token válido:** `valid-token` → `200 OK`
- **Token inválido:** `invalid-token` → `401 Unauthorized`
- **Sin token:** → `401 Unauthorized`

**Ejemplo con token válido:**
```bash
curl -H "Authorization: Bearer valid-token" http://localhost:8000/validate-token
```

**Respuesta:** `200 OK`
```json
{
  "message": "Token validated",
  "user_id": "user1"
}
```

### Expect 401

```
GET /expect-401
Authorization: Bearer <token> (opcional)
```

**DSL keyword:** `expect 401`

- **Sin token:** → `401 Unauthorized`
- **Token inválido:** `invalid-token` → `401 Unauthorized`
- **Token válido:** `valid-token` → `200 OK` (pero el DSL espera 401)

**Ejemplo sin token:**
```bash
curl http://localhost:8000/expect-401
```

**Respuesta:** `401 Unauthorized`
```json
{
  "detail": "Missing authentication token"
}
```

### Access Denied

```
GET /access-denied
Authorization: Bearer <token>
```

**DSL keyword:** `access denied`

- **Token admin:** `valid-token` → `200 OK`
- **Token usuario:** `user-token` → `403 Forbidden`
- **Sin token:** → `401 Unauthorized`

**Ejemplo con token de usuario (espera 403):**
```bash
curl -H "Authorization: Bearer user-token" http://localhost:8000/access-denied
```

**Respuesta:** `403 Forbidden`
```json
{
  "detail": "Access denied"
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
curl -H "Authorization: Bearer valid-token" http://localhost:8000/validate-token

# Token inválido (debe retornar 401)
curl -H "Authorization: Bearer invalid-token" http://localhost:8000/validate-token

# Sin token (debe retornar 401)
curl http://localhost:8000/validate-token
```

### Probar "expect 401"

```bash
# Sin token (debe retornar 401)
curl http://localhost:8000/expect-401

# Token inválido (debe retornar 401)
curl -H "Authorization: Bearer invalid-token" http://localhost:8000/expect-401
```

### Probar "access denied"

```bash
# Token de usuario en endpoint admin (debe retornar 403)
curl -H "Authorization: Bearer user-token" http://localhost:8000/access-denied

# Token admin (debe retornar 200)
curl -H "Authorization: Bearer valid-token" http://localhost:8000/access-denied
```

## Documentación Interactiva

Una vez que el servidor esté corriendo:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Mapeo DSL Keywords

| DSL Keyword | Endpoint | Caso de Prueba |
|------------|----------|----------------|
| `validate token` | `/validate-token` | Token válido → 200 |
| `expect 401` | `/expect-401` | Sin token o token inválido → 401 |
| `access denied` | `/access-denied` | Token usuario en endpoint admin → 403 |

## Códigos de Estado

- `200 OK` - Token válido y acceso autorizado
- `401 Unauthorized` - Token inválido o faltante
- `403 Forbidden` - Token válido pero sin permisos

## Desarrollo

Este API es parte del proyecto Vhape MVP y se usa internamente para pruebas BDD. No está diseñado para uso en producción.
