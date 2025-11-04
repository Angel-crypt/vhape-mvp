# Parser Implementation

## Resumen

Se ha implementado el parser DSL usando Lark para reconocer y parsear los pasos de Gherkin definidos.

## Archivos Creados

### 1. `vhape/parser/grammar.lark`

Gramática Lark que define la sintaxis del DSL:

- **Given steps**: Reconoce diferentes tipos de tokens (valid, admin, user, invalid, none)
- **When steps**: Reconoce requests a endpoints
- **Then steps**: Reconoce validaciones (validate_token, expect_401, access_denied, access_allowed)

### 2. `vhape/parser/parse.py`

Implementación del parser:

- **StepParser**: Clase principal para parsear pasos
- **parse_step()**: Función de conveniencia para parsear un paso
- **DSLParseError**: Excepción personalizada para errores de parsing

### 3. `vhape/parser/__init__.py`

Módulo de exportación del parser.

### 4. `test/test_parser.py`

Tests unitarios para validar el parser.

## Estructura de Salida

El parser retorna diccionarios estructurados:

### Given Steps

```python
{
    'type': 'given',
    'token_type': 'valid' | 'admin' | 'user' | 'invalid' | 'none'
}
```

### When Steps

```python
{
    'type': 'when',
    'endpoint': '/api/users/me'
}
```

### Then Steps

```python
{
    'type': 'then',
    'validation': 'validate_token' | 'expect_401' | 'access_denied' | 'access_allowed'
}
```

## Ejemplos de Uso

```python
from vhape.parser import parse_step

# Parsear un Given step
result = parse_step("Given I have a valid token")
# {'type': 'given', 'token_type': 'valid'}

# Parsear un When step
result = parse_step('When I send a request to "/api/users/me"')
# {'type': 'when', 'endpoint': '/api/users/me'}

# Parsear un Then step
result = parse_step("Then the response should validate token")
# {'type': 'then', 'validation': 'validate_token'}
```

## Características

- ✅ Case-insensitive (acepta mayúsculas y minúsculas)
- ✅ Manejo de errores con excepciones personalizadas
- ✅ Estructura de datos clara y consistente
- ✅ Fácil de extender para nuevos keywords
