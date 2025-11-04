# Vhape DSL - Sintaxis Mínima

## Visión General

El DSL de Vhape está basado en Gherkin y permite describir escenarios de seguridad de APIs de forma simple y natural. Está diseñado para usuarios no técnicos que necesitan validar la seguridad de sus APIs.

## Estructura Básica

### Feature (Característica)

Describe qué funcionalidad se está probando.

```gherkin
Feature: Nombre de la característica
  Descripción opcional de la característica
```

### Scenario (Escenario)

Describe un caso de prueba específico.

```gherkin
Scenario: Nombre del escenario
  Pasos del escenario
```

## Keywords DSL Principales

### 1. `validate token`

Valida que un token de autenticación es válido.

**Ejemplo:**

```gherkin
Given I have a valid token
When I send a request to "/api/users/me"
Then the response should validate token
```

### 2. `expect 401`

Verifica que la respuesta es 401 Unauthorized.

**Ejemplo:**

```gherkin
Given I have no token
When I send a request to "/api/users/me"
Then the response should expect 401
```

O con token inválido:

```gherkin
Given I have an invalid token
When I send a request to "/api/users/me"
Then the response should expect 401
```

### 3. `access denied`

Verifica que la respuesta es 403 Forbidden (acceso denegado).

**Ejemplo:**

```gherkin
Given I have a user token
When I send a request to "/api/admin/users"
Then the response should access denied
```

### 4. `access allowed`

Verifica que la respuesta es 200 OK (acceso permitido).

**Ejemplo:**

```gherkin
Given I have an admin token
When I send a request to "/api/admin/users"
Then the response should access allowed
```

## Estructura de Pasos

### Given (Dado)

Define el estado inicial o contexto.

**Tokens disponibles:**

- `valid token` / `admin token` - Token válido con rol admin
- `user token` - Token válido con rol usuario
- `invalid token` - Token inválido
- `no token` / `missing token` - Sin token

**Ejemplos:**

```gherkin
Given I have a valid token
Given I have an admin token
Given I have a user token
Given I have an invalid token
Given I have no token
```

### When (Cuando)

Define la acción a realizar.

**Formato:**

```gherkin
When I send a request to "<endpoint>"
```

**Ejemplos:**

```gherkin
When I send a request to "/api/users/me"
When I send a request to "/api/admin/users"
```

### Then (Entonces)

Define el resultado esperado.

**Formato:**

```gherkin
Then the response should <keyword>
```

**Keywords disponibles:**

- `validate token` - Token válido (200 OK)
- `expect 401` - No autorizado (401)
- `access denied` - Acceso denegado (403)
- `access allowed` - Acceso permitido (200 OK)

**Ejemplos:**

```gherkin
Then the response should validate token
Then the response should expect 401
Then the response should access denied
Then the response should access allowed
```

## Ejemplos Completos

### Ejemplo 1: Validar Token

```gherkin
Feature: User Authentication
  As a developer
  I want to validate API authentication
  So that I can ensure my API is secure

  Scenario: Valid token should grant access
    Given I have a valid token
    When I send a request to "/api/users/me"
    Then the response should validate token
```

### Ejemplo 2: Token Inválido

```gherkin
  Scenario: Invalid token should return 401
    Given I have an invalid token
    When I send a request to "/api/users/me"
    Then the response should expect 401
```

### Ejemplo 3: Sin Token

```gherkin
  Scenario: Missing token should return 401
    Given I have no token
    When I send a request to "/api/users/me"
    Then the response should expect 401
```

### Ejemplo 4: Acceso Denegado

```gherkin
Feature: Admin Authorization
  As a developer
  I want to validate admin authorization
  So that I can ensure admin endpoints are protected

  Scenario: User token should be denied access to admin endpoint
    Given I have a user token
    When I send a request to "/api/admin/users"
    Then the response should access denied
```

### Ejemplo 5: Acceso Permitido

```gherkin
  Scenario: Admin token should allow access to admin endpoint
    Given I have an admin token
    When I send a request to "/api/admin/users"
    Then the response should access allowed
```

## Reglas de Sintaxis

1. **Case-insensitive**: Las keywords pueden escribirse en mayúsculas o minúsculas.
2. **Espacios**: Los espacios son significativos solo dentro de las frases.
3. **Comillas**: Los endpoints deben ir entre comillas dobles.
4. **Orden**: Los pasos deben seguir el orden Given → When → Then.

## Extensibilidad

La sintaxis está diseñada para ser extensible. Futuras versiones pueden agregar:

- Múltiples headers
- Métodos HTTP (GET, POST, PUT, DELETE)
- Validación de body de respuesta
- Timeouts
- Múltiples requests en un escenario

## Notas de Implementación

- El parser debe ser tolerante a variaciones menores (espacios extra, mayúsculas/minúsculas)
- Los endpoints pueden ser relativos o absolutos
- Los tokens se referencian por nombre, no por valor (el sistema los resuelve internamente)
