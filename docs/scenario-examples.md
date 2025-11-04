# Ejemplos Funcionales de Escenarios - Vhape DSL

Este documento describe los ejemplos funcionales de escenarios creados para demostrar el uso del DSL de Vhape en diferentes contextos de testing de seguridad API.

## Estructura de Archivos Feature

Los escenarios están organizados en varios archivos `.feature` ubicados en el directorio `features/`:

### 1. `auth.feature` - Escenarios Básicos de Autenticación

Contiene los casos básicos y fundamentales de autenticación y autorización:

- ✅ Token válido permite acceso a perfil de usuario
- ✅ Token inválido retorna 401
- ✅ Token faltante retorna 401
- ✅ Token de usuario denegado en endpoint de admin
- ✅ Token de admin permite acceso a endpoint de admin

**Uso**: Ideal para smoke tests y validación básica del sistema.

### 2. `api_security.feature` - Escenarios Comprehensivos de Seguridad

Incluye escenarios más complejos usando `Scenario Outline` para pruebas parametrizadas:

- **Token validation for different token types**: Prueba todos los tipos de token con diferentes endpoints
- **Role-based access control**: Valida el control de acceso basado en roles
- **Health check accessibility**: Verifica que el endpoint de health no requiera autenticación
- **Negative test cases**: Pruebas de seguridad negativas

**Uso**: Para pruebas de regresión y validación exhaustiva de seguridad.

### 3. `workflow.feature` - Flujos de Trabajo Completos

Simula flujos de trabajo completos de autenticación:

- Flujo de usuario autenticado exitoso
- Intento de acceso no autorizado
- Flujo de admin autorizado
- Flujo de usuario no autorizado intentando acceso admin
- Flujo sin autenticación

**Uso**: Para pruebas end-to-end (E2E) y validación de flujos de usuario.

### 4. `edge_cases.feature` - Casos Límite

Cubre casos límite y condiciones de borde:

- Intentos múltiples con tokens inválidos
- Accesos repetidos a endpoints protegidos
- Tokens válidos en diferentes contextos
- Comportamiento con endpoints de health check

**Uso**: Para pruebas de robustez y manejo de casos excepcionales.

## Cómo Usar los Escenarios

### Ejecutar Todos los Escenarios

```bash
behave features/
```

### Ejecutar un Feature Específico

```bash
behave features/auth.feature
behave features/api_security.feature
behave features/workflow.feature
behave features/edge_cases.feature
```

### Ejecutar Escenarios con Tags

```bash
# Solo escenarios de autenticación
behave --tags=@authentication

# Solo escenarios de autorización
behave --tags=@authorization

# Solo smoke tests
behave --tags=@smoke

# Solo pruebas negativas
behave --tags=@negative
```

### Ejecutar un Escenario Específico

```bash
behave features/auth.feature -n "Valid token should grant access"
```

## Estructura de un Escenario

Cada escenario sigue la estructura Gherkin estándar:

```gherkin
Feature: Nombre del Feature
  As a [rol]
  I want to [objetivo]
  So that [beneficio]

  Scenario: Descripción del escenario
    Given I have <tipo_token> token
    When I send a request to "<endpoint>"
    Then the response should <validación>
```

## Tipos de Tokens Disponibles

- `a valid token` - Token válido (admin)
- `an admin token` - Token de administrador
- `a user token` - Token de usuario regular
- `an invalid token` - Token inválido
- `no token` / `a missing token` - Sin token

## Endpoints Disponibles

- `/api/health` - Health check (público)
- `/api/users/me` - Perfil de usuario (requiere autenticación)
- `/api/admin/users` - Lista de usuarios (requiere rol admin)

## Validaciones Disponibles

- `validate token` - Espera 200 OK con datos válidos
- `expect 401` - Espera 401 Unauthorized
- `access denied` - Espera 403 Forbidden
- `access allowed` - Espera 200 OK con acceso permitido

## Crear Nuevos Escenarios

Para crear un nuevo escenario:

1. **Elige el archivo feature apropiado** o crea uno nuevo en `features/`
2. **Define el Feature** con descripción clara
3. **Escribe el Scenario** usando los pasos disponibles:
   - `Given I have <tipo> token`
   - `When I send a request to "<endpoint>"`
   - `Then the response should <validación>`
4. **Ejecuta el escenario** para validar que funciona

### Ejemplo de Nuevo Escenario

```gherkin
Feature: Nuevo Feature
  As a tester
  I want to test something new
  So that I can validate it

  Scenario: Nuevo escenario de prueba
    Given I have a valid token
    When I send a request to "/api/users/me"
    Then the response should validate token
```

## Tags Disponibles

Los escenarios pueden usar tags para organización:

- `@smoke` - Pruebas de smoke test
- `@authentication` - Relacionado con autenticación
- `@authorization` - Relacionado con autorización
- `@role-based` - Control de acceso basado en roles
- `@security` - Pruebas de seguridad
- `@negative` - Pruebas negativas
- `@edge-cases` - Casos límite

## Prerequisitos

Antes de ejecutar los escenarios, asegúrate de:

1. ✅ El API dummy está corriendo en `http://localhost:8000`
2. ✅ El entorno virtual está activado
3. ✅ Todas las dependencias están instaladas (`pip install -r requirements.txt`)

Para iniciar el API dummy:

```bash
./api_dummy/run.sh
# o
python api_dummy/run.py
```

## Troubleshooting

### Error: "API server is not running"

Solución: Inicia el API dummy antes de ejecutar los tests.

### Error: "Failed to parse step"

Solución: Verifica que el paso siga exactamente la sintaxis del DSL. Consulta `docs/dsl-syntax.md` para la sintaxis completa.

### Error: "No response available"

Solución: Asegúrate de que el paso `When` se ejecute antes del paso `Then`.

## Próximos Pasos

- Agregar más endpoints al API dummy para expandir los casos de prueba
- Implementar soporte para métodos HTTP adicionales (POST, PUT, DELETE)
- Agregar validaciones de cuerpo de respuesta más complejas
- Implementar escenarios de rate limiting y otros aspectos de seguridad

