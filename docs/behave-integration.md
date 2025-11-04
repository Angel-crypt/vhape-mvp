# Integración con Behave - T3

## Resumen

Se ha integrado el parser DSL con Behave para ejecutar escenarios de testing de seguridad de APIs.

## Archivos Creados

### 1. `vhape/steps/auth_steps.py`
Step definitions que integran el parser DSL con Behave:

- **Given steps**: Configuran el token de autenticación usando el parser
- **When steps**: Envían requests HTTP al API dummy
- **Then steps**: Validan las respuestas según los DSL keywords

### 2. `vhape/steps/environment.py`
Configuración de entorno de Behave:

- Verifica que el API server esté accesible
- Inicializa el contexto antes de cada escenario
- Limpia el contexto después de cada escenario

### 3. `behave.ini`
Configuración de Behave:

- Ubicación de step definitions
- Ubicación de feature files
- Formato de salida
- Configuración de verbose

## Funcionamiento

### Flujo de Ejecución

1. **Given Step**: 
   - Behave ejecuta el step "Given I have a valid token"
   - El step definition usa el parser DSL para interpretar el paso
   - El parser retorna `{'type': 'given', 'token_type': 'valid'}`
   - El step definition mapea el token type al token real y lo almacena en `context.token`

2. **When Step**:
   - Behave ejecuta el step 'When I send a request to "/api/users/me"'
   - El step definition usa el parser DSL para extraer el endpoint
   - Se envía un GET request al API dummy con el token (si existe)
   - La respuesta se almacena en `context.response`

3. **Then Step**:
   - Behave ejecuta el step "Then the response should validate token"
   - El step definition usa el parser DSL para interpretar la validación
   - Se valida el status code y contenido de la respuesta
   - Si falla, Behave marca el escenario como fallido

## Mapeo de Tokens

El step definition mapea los tokens DSL a los tokens reales del API:

| DSL Token Type | API Token | Descripción |
|----------------|-----------|-------------|
| `valid` | `valid-token` | Token admin |
| `admin` | `valid-token` | Token admin (igual que valid) |
| `user` | `user-token` | Token usuario |
| `invalid` | `invalid-token` | Token inválido |
| `none` | `None` | Sin token |

## Validaciones Implementadas

### `validate_token`
- **Status esperado**: 200 OK
- **Validación**: Response debe contener `user_id` o `message`

### `expect_401`
- **Status esperado**: 401 Unauthorized
- **Validación**: Response debe contener `detail`

### `access_denied`
- **Status esperado**: 403 Forbidden
- **Validación**: Response debe contener `detail` con "Access denied"

### `access_allowed`
- **Status esperado**: 200 OK
- **Validación**: Response debe contener `users` o `message`

## Configuración

### Variable de Entorno

El API base URL puede configurarse con la variable de entorno `VHAPE_API_URL`:

```bash
export VHAPE_API_URL=http://localhost:8000
behave
```

O por defecto usa: `http://localhost:8000`

## Ejecutar Tests

### Prerrequisitos

1. API dummy debe estar corriendo:
   ```bash
   ./api_dummy/run.sh
   ```

2. Dependencias instaladas:
   ```bash
   pip install -r requirements.txt
   ```

### Ejecutar Todos los Escenarios

```bash
behave
```

### Ejecutar un Feature Específico

```bash
behave features/auth.feature
```

### Ejecutar un Escenario Específico

```bash
behave features/auth.feature -n "Valid token should grant access"
```

### Modo Verbose

```bash
behave -v
```

## Estructura de Context

El contexto de Behave almacena:

- `context.token`: Token actual (string o None)
- `context.token_type`: Tipo de token DSL ('valid', 'admin', 'user', 'invalid', 'none')
- `context.response`: Objeto Response de requests
- `context.response_status`: Status code HTTP
- `context.response_data`: JSON response data (dict)

## Fallback Parsing

Si el parser DSL falla por alguna razón, los step definitions tienen un fallback que intenta determinar el tipo directamente del texto, proporcionando mayor robustez.

## Próximos Pasos

El sistema está listo para ejecutar escenarios end-to-end. Los pasos siguientes serían:
- T4: Crear ejemplos funcionales adicionales
- T5: Realizar pruebas end-to-end completas

