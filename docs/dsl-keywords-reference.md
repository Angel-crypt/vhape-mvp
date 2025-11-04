# Vhape DSL - Referencia de Keywords

## Resumen de Keywords DSL

Esta es una referencia rápida de todas las keywords disponibles en el DSL de Vhape.

## Keywords de Contexto (Given)

### Tokens

| Keyword | Descripción | Resultado Esperado |
|---------|-------------|-------------------|
| `I have a valid token` | Token válido (admin) | Permite acceso |
| `I have an admin token` | Token con rol admin | Permite acceso admin |
| `I have a user token` | Token con rol usuario | Permite acceso usuario |
| `I have an invalid token` | Token inválido | Retorna 401 |
| `I have no token` | Sin token | Retorna 401 |
| `I have a missing token` | Token faltante | Retorna 401 |

## Keywords de Acción (When)

### Request

| Keyword | Formato | Ejemplo |
|---------|---------|---------|
| `I send a request to "<endpoint>"` | Endpoint entre comillas | `"/api/users/me"` |

## Keywords de Validación (Then)

### Resultados

| Keyword | Descripción | Código HTTP Esperado |
|---------|-------------|---------------------|
| `validate token` | Token válido | 200 OK |
| `expect 401` | No autorizado | 401 Unauthorized |
| `access denied` | Acceso denegado | 403 Forbidden |
| `access allowed` | Acceso permitido | 200 OK |

## Mapeo de Keywords a Endpoints

Basado en el API dummy actual:

| DSL Keyword | Endpoint | Caso de Prueba |
|------------|----------|----------------|
| `validate token` | `/api/users/me` | Token válido → 200 |
| `expect 401` | `/api/users/me` | Sin token o token inválido → 401 |
| `access denied` | `/api/admin/users` | Token usuario en endpoint admin → 403 |
| `access allowed` | `/api/admin/users` | Token admin en endpoint admin → 200 |

## Ejemplos Rápidos

### Validar Token

```gherkin
Given I have a valid token
When I send a request to "/api/users/me"
Then the response should validate token
```

### Esperar 401

```gherkin
Given I have no token
When I send a request to "/api/users/me"
Then the response should expect 401
```

### Acceso Denegado

```gherkin
Given I have a user token
When I send a request to "/api/admin/users"
Then the response should access denied
```

### Acceso Permitido

```gherkin
Given I have an admin token
When I send a request to "/api/admin/users"
Then the response should access allowed
```
