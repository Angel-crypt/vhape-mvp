# Análisis Completo del Proyecto Vhape MVP

## 1. Tabla de Tecnologías y Componentes

| Tecnología / Componente | Archivo / Ruta en el Proyecto | Descripción breve de su función |
|------------------------|-------------------------------|--------------------------------|
| **Lark Parser (DSL)** | `vhape/parser/grammar.lark` | Define la gramática del DSL para parsear pasos Gherkin (Given/When/Then) |
| **Lark Parser (DSL)** | `vhape/parser/parse.py` | Implementa el parser que interpreta los pasos Gherkin y extrae información estructurada (tokens, endpoints, validaciones) |
| **Behave (BDD y Gherkin)** | `vhape/behave.ini` | Archivo de configuración de Behave que define rutas de features, formato de salida y opciones de ejecución |
| **Behave (BDD y Gherkin)** | `features/*.feature` | Archivos de escenarios Gherkin que definen los casos de prueba en lenguaje natural (auth.feature, workflow.feature, etc.) |
| **Behave (BDD y Gherkin)** | `features/steps/environment.py` | Hooks de Behave (before_all, after_all, after_scenario) que inicializan el contexto, verifican la API y generan reportes |
| **Behave (BDD y Gherkin)** | `features/steps/auth_steps.py` | Definiciones de pasos Behave que implementan Given/When/Then, usan el parser DSL y ejecutan peticiones HTTP |
| **FastAPI (API dummy)** | `api_dummy/main.py` | Servidor FastAPI que simula una API REST con endpoints protegidos para probar autenticación y autorización |
| **Uvicorn (servidor para API dummy)** | `api_dummy/run.py` | Script Python que inicia el servidor Uvicorn para ejecutar la API dummy en localhost:8000 |
| **Uvicorn (servidor para API dummy)** | `api_dummy/run.sh` | Script bash alternativo para iniciar el servidor Uvicorn con configuración del entorno virtual |
| **JSON (generación de reportes)** | `vhape/reporting/summary.py` | Clase TestSummary que recopila resultados de tests, genera estadísticas y guarda reportes en formato JSON |
| **JSON (generación de reportes)** | `tests/results/summary_*.json` | Archivos JSON generados automáticamente con resultados detallados de ejecución de tests, incluyendo issues de seguridad |
| **HTML (generación de reportes)** | `tests/e2e/html_report_generator.py` | Generador de reportes HTML modernos e interactivos a partir de archivos JSON, incluye CSS y JavaScript para búsqueda y filtrado |
| **HTML (generación de reportes)** | `tests/results/summary_*.html` | Archivos HTML generados automáticamente con reportes visuales interactivos, incluyen estadísticas, features, scenarios y security issues |
| **pytest (unitarias)** | `tests/unit/test_parser.py` | Tests unitarios que validan el funcionamiento del parser DSL con diferentes tipos de pasos Gherkin |
| **pytest (unitarias)** | `tests/unit/test_summary.py` | Tests unitarios que validan la funcionalidad de la clase TestSummary, incluyendo estadísticas y generación de reportes |
| **pytest (unitarias)** | `tests/unit/test_auth_steps.py` | Tests unitarios que validan la lógica de mapeo de tokens, construcción de headers y validación sin hacer requests HTTP reales |
| **Postman (colecciones)** | `api_dummy/postman/Vhape_Dummy_API.postman_collection.json` | Colección de Postman con requests preconfigurados para probar manualmente los endpoints de la API dummy |
| **Postman (colecciones)** | `api_dummy/postman/Vhape_Dummy_API.postman_environment.json` | Variables de entorno de Postman (base_url) para usar con la colección |
| **requests** | `features/steps/auth_steps.py` | Biblioteca HTTP usada en los steps de Behave para enviar peticiones GET a los endpoints de la API |
| **requests** | `features/steps/environment.py` | Usada para verificar el estado de salud de la API antes de ejecutar los tests |
| **Script de ejecución de tests** | `tests/e2e/run_e2e_tests.py` | Script principal que ejecuta Behave, parsea resultados, genera reportes JSON y HTML, muestra resumen en consola y abre el reporte HTML en el navegador |
| **Configuración de tokens** | `features/steps/auth_steps.py` (TOKEN_MAP) | Diccionario que mapea tipos de tokens del DSL ('valid', 'admin', 'user', 'invalid', 'none') a tokens reales de la API |
| **Configuración de URL de API** | `features/steps/environment.py` (VHAPE_API_URL) | Variable de entorno que define la URL base de la API (por defecto: <http://localhost:8000>) |
| **Configuración de URL de API** | `features/steps/auth_steps.py` (API_BASE_URL) | Variable de entorno que define la URL base de la API para las peticiones HTTP en los steps |

---

## 2. Diagrama de Flujo de Ejecución del Proyecto

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CONFIGURACIÓN INICIAL DEL USUARIO                     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────┐
        │ 1. Configurar URL de API                  │
        │    - Variable de entorno: VHAPE_API_URL   │
        │    - O usar default: http://localhost:8000│
        │    - Ubicación: features/steps/           │
        │      environment.py y auth_steps.py       │
        └───────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────┐
        │ 2. Configurar Tokens                      │
        │    - Archivo: features/steps/auth_steps.py│
        │    - Diccionario TOKEN_MAP:               │
        │      'valid' → 'valid-token'              │
        │      'admin' → 'valid-token'              │
        │      'user' → 'user-token'                │
        │      'invalid' → 'invalid-token'          │
        │      'none' → None                        │
        └───────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    INICIO DE LA API DUMMY (OPCIONAL)                     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────┐
        │ 3. Iniciar API Dummy                      │
        │    - Script: api_dummy/run.py             │
        │      o api_dummy/run.sh                   │
        │    - Servidor: Uvicorn                    │
        │    - Framework: FastAPI (api_dummy/main.py)│
        │    - Puerto: 8000                         │
        │    - Endpoints:                           │
        │      • /api/health                        │
        │      • /api/users/me                      │
        │      • /api/admin/users                   │
        └───────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    EJECUCIÓN DE TESTS                                    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────┐
        │ 4. Ejecutar Tests                         │
        │    - Opción A:                            │
        │      python tests/e2e/                    │
        │        run_e2e_tests.py                   │
        │    - Opción B:                            │
        │      behave features/                     │
        └───────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────┐
        │ 5. Behave lee configuración               │
        │    - Archivo: vhape/behave.ini            │
        │    - Define:                              │
        │      • paths = features                   │
        │      • format = pretty                    │
        │      • steps_dir = features/steps         │
        └───────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────┐
        │ 6. Behave carga environment.py            │
        │    - Archivo: features/steps/environment.py│
        │    - Hook: before_all()                   │
        │      • Verifica API en /api/health        │
        │      • Inicializa TestSummary             │
        │      • Configura context.api_url          │
        └───────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────┐
        │ 7. Behave lee archivos .feature           │
        │    - features/auth.feature                │
        │    - features/workflow.feature            │
        │    - features/failure_scenarios.feature   │
        │    - features/edge_cases.feature          │
        │    - features/api_security.feature        │
        │    - Formato: Gherkin (Given/When/Then)   │
        └───────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────┐
        │ 8. Para cada Scenario en .feature:        │
        │    Ejemplo:                               │
        │    Given I have a valid token             │
        │    When I send a request to "/api/users/me"│
        │    Then the response should validate token│
        └───────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────┐
        │ 9. Behave ejecuta Step: Given             │
        │    - Archivo: features/steps/auth_steps.py│
        │    - Función: step_given_token()          │
        │    - Flujo:                               │
        │      1. Construye texto completo:         │
        │         "Given I have a valid token"      │
        │      2. Llama al parser DSL               │
        └───────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────┐
        │ 10. Parser DSL procesa el paso            │
        │     - Archivo: vhape/parser/parse.py      │
        │     - Función: parse_step()               │
        │     - Lee gramática:                      │
        │       vhape/parser/grammar.lark           │
        │     - Retorna:                            │
        │       {'type': 'given',                   │
        │        'token_type': 'valid'}             │
        └───────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────┐
        │ 11. Step mapea token_type a token real    │
        │     - Usa TOKEN_MAP en auth_steps.py      │
        │     - 'valid' → 'valid-token'             │
        │     - Guarda en context.token             │
        └───────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────┐
        │ 12. Behave ejecuta Step: When             │
        │     - Función: step_when_request()        │
        │     - Flujo:                              │
        │       1. Parsea: "When I send a request   │
        │          to \"/api/users/me\""            │
        │       2. Extrae endpoint: "/api/users/me" │
        │       3. Construye URL completa:          │
        │          API_BASE_URL + endpoint          │
        │       4. Prepara headers:                 │
        │          Authorization: Bearer <token>    │
        │       5. Envía GET request (requests)     │
        │       6. Guarda response en context       │
        └───────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────┐
        │ 13. API Dummy procesa request             │
        │     - Archivo: api_dummy/main.py          │
        │     - Endpoint: /api/users/me             │
        │     - Valida token con get_current_user() │
        │     - Retorna 200 OK o 401 Unauthorized   │
        └───────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────┐
        │ 14. Behave ejecuta Step: Then             │
        │     - Función: step_then_validate()       │
        │     - Flujo:                              │
        │       1. Parsea: "Then the response       │
        │          should validate token"           │
        │       2. Extrae validación:               │
        │          'validate_token'                 │
        │       3. Valida response_status:          │
        │          • validate_token → espera 200    │
        │          • expect_401 → espera 401        │
        │          • access_denied → espera 403     │
        │          • access_allowed → espera 200    │
        │       4. Si falla, registra security issue│
        └───────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────┐
        │ 15. Hooks de Behave registran resultados  │
        │     - after_step():                       │
        │       • Registra paso en TestSummary      │
        │     - after_scenario():                   │
        │       • Registra scenario en TestSummary  │
        │       • Limpia context (token, response)  │
        │     - after_feature():                    │
        │       • Registra feature en TestSummary   │
        └───────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────┐
        │ 16. Hook after_all() finaliza             │
        │     - Archivo: features/steps/            │
        │       environment.py                      │
        │     - Flujo:                              │
        │       1. Llama test_summary.finalize()    │
        │       2. Calcula estadísticas             │
        │       3. Muestra resumen en consola       │
        │       4. Genera JSON report               │
        └───────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────┐
        │ 17. TestSummary genera reporte JSON       │
        │     - Archivo: vhape/reporting/summary.py │
        │     - Método: save_json()                 │
        │     - Ubicación: tests/results/           │
        │       summary_YYYYMMDD_HHMMSS.json        │
        │     - Contenido:                          │
        │       • start_time, end_time              │
        │       • statistics (features, scenarios,  │
        │         steps, security_issues)           │
        │       • features[]                        │
        │       • scenarios[]                       │
        │       • security_issues[]                 │
        └───────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────┐
        │ 18. Resumen mostrado en consola           │
        │     - Features: total, passed, failed     │
        │     - Scenarios: total, passed, failed    │
        │     - Steps: total, passed, failed        │
        │     - Security Issues: count y detalles   │
        │     - Success Rate: porcentaje            │
        │     - Duration: tiempo de ejecución       │
        └───────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────┐
        │ 19. Si se usó run_e2e_tests.py:          │
        │     - Parsea output de Behave             │
        │     - Mejora reporte con datos adicionales│
        │     - Muestra resumen mejorado            │
        └───────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────┐
        │ 20. Generador HTML crea reporte visual    │
        │     - Archivo: tests/e2e/                 │
        │       html_report_generator.py            │
        │     - Función: generate_html_report()     │
        │     - Flujo:                              │
        │       1. Lee archivo JSON generado        │
        │       2. Genera HTML con CSS embebido     │
        │       3. Incluye JavaScript para:         │
        │          • Búsqueda de features/scenarios │
        │          • Filtrado (All/Passed/Failed)   │
        │       4. Agrupa scenarios por feature     │
        │       5. Calcula status badges            │
        │       6. Resalta security issues          │
        │     - Ubicación: tests/results/           │
        │       summary_YYYYMMDD_HHMMSS.html        │
        │     - Características:                    │
        │       • Diseño moderno y responsive       │
        │       • Dashboard con estadísticas        │
        │       • Sección de security issues        │
        │       • Lista de features y scenarios     │
        │       • Búsqueda y filtrado interactivo   │
        └───────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────┐
        │ 21. Reporte HTML se abre automáticamente  │
        │     - run_e2e_tests.py abre el navegador  │
        │     - Usa webbrowser.open()               │
        │     - Muestra reporte visual completo     │
        └───────────────────────────────────────────┘
                                    │
                                    ▼
                            ┌───────────────┐
                            │   FIN         │
                            └───────────────┘
```

---

## Resumen del Flujo de Datos

### Flujo Principal

1. **Configuración** → Usuario define URL de API y tokens en `auth_steps.py`
2. **Inicio API** → Se inicia la API dummy con Uvicorn (opcional, puede estar corriendo)
3. **Ejecución** → Se ejecuta `run_e2e_tests.py` o `behave` directamente
4. **Behave** → Lee `.feature` files y ejecuta steps definidos en `auth_steps.py`
5. **Parser DSL** → Cada step Given/When/Then es parseado por `parse.py` usando `grammar.lark`
6. **HTTP Requests** → Los steps When envían requests a la API usando `requests`
7. **Validación** → Los steps Then validan las respuestas y detectan issues de seguridad
8. **Reporte JSON** → `TestSummary` recopila resultados y genera JSON en `tests/results/`
9. **Reporte HTML** → `html_report_generator.py` genera reporte visual interactivo desde JSON
10. **Visualización** → Reporte HTML se abre automáticamente en el navegador

### Puntos Clave de Integración

- **Parser DSL ↔ Steps**: `auth_steps.py` llama a `parse_step()` de `vhape/parser/parse.py`
- **Steps ↔ API**: `auth_steps.py` usa `requests` para llamar a `api_dummy/main.py`
- **Behave ↔ Reporting**: `environment.py` usa `TestSummary` de `vhape/reporting/summary.py`
- **JSON ↔ HTML**: `html_report_generator.py` lee JSON y genera HTML con CSS/JavaScript embebido
- **Configuración**: Variables de entorno (`VHAPE_API_URL`) y `TOKEN_MAP` en `auth_steps.py`

---

## 3. Archivos de Tests y Reportes

### 3.1 Tests Unitarios

| Archivo | Descripción | Cobertura |
|---------|-------------|-----------|
| `tests/unit/test_parser.py` | Tests del parser DSL | Valida parsing de Given/When/Then steps, manejo de errores, extracción de tokens/endpoints/validaciones |
| `tests/unit/test_summary.py` | Tests de TestSummary | Valida recopilación de features/scenarios/steps, cálculo de estadísticas, generación de JSON |
| `tests/unit/test_auth_steps.py` | Tests de lógica de autenticación | Valida mapeo de tokens (TOKEN_MAP), construcción de headers, validación de respuestas (sin HTTP real) |

### 3.2 Tests E2E (End-to-End)

| Archivo | Descripción | Escenarios |
|---------|-------------|------------|
| `features/auth.feature` | Tests básicos de autenticación | 5 scenarios: valid/invalid/missing tokens, admin/user access |
| `features/api_security.feature` | Tests comprehensivos de seguridad | 13 scenarios: validación de tokens, autorización, edge cases |
| `features/workflow.feature` | Tests de flujos completos | 5 scenarios: workflows de autenticación end-to-end |
| `features/edge_cases.feature` | Tests de casos límite | 5 scenarios: múltiples intentos, endpoints no existentes, health check |
| `features/failure_scenarios.feature` | Tests que intencionalmente fallan | 8 scenarios: validación del sistema de reportes con fallos |

**Total de Scenarios:** ~36 scenarios distribuidos en 5 feature files

### 3.3 Archivos de Reportes Generados

| Tipo | Patrón de Nombre | Ubicación | Contenido |
|------|------------------|-----------|-----------|
| **JSON** | `summary_YYYYMMDD_HHMMSS.json` | `tests/results/` | Datos estructurados: statistics, features, scenarios, steps, security_issues |
| **HTML** | `summary_YYYYMMDD_HHMMSS.html` | `tests/results/` | Reporte visual interactivo con CSS/JavaScript embebido, búsqueda y filtrado |

### 3.4 Estructura del Reporte HTML

El reporte HTML generado incluye:

1. **Header**: Logo VHAPE, fecha de generación, archivo fuente JSON
2. **Overview Section**:
   - Status badge (success/warning/danger)
   - Grid de estadísticas: Success Rate, Duration, Features, Scenarios, Steps, Security Issues
3. **Security Issues Section** (si hay issues):
   - Lista de issues con severity (high/medium/low)
   - Mensaje, step asociado, timestamp
4. **Features & Scenarios Section**:
   - Lista de features agrupadas
   - Scenarios dentro de cada feature
   - Badges de status (passed/failed)
   - Búsqueda y filtrado (All/Passed/Failed)
5. **Footer**: Información de generación, tiempo de ejecución

**Características Técnicas:**

- CSS embebido (responsive design, gradientes, animaciones)
- JavaScript embebido (búsqueda en tiempo real, filtrado, smooth scroll)
- Sin dependencias externas (todo embebido en el HTML)
- Compatible con navegadores modernos

---

**Documento actualizado:** 2025-01-27  
**Versión del análisis:** 2.0 (incluye reportes HTML y tests completos)

> 📖 **Para información detallada sobre componentes, ejecución de tests y reportes**, consulta [`README.md`](README.md)
