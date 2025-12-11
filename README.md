# Sportclub Challenge: Backend API (FastAPI y Docker)

Este proyecto contiene un servicio de Backend desarrollado en **FastAPI** (Python). La API consume una API externa, aplica lógica de negocio  y expone los endpoints para el consumo del Frontend de React.

## Tecnologías Utilizadas

* **Lenguaje:** Python 3.14.0
* **Framework Web:** FastAPI
* **Contenedores:** Docker y Docker Compose
* **Librerías Clave:** `httpx` (para consumo de APIs externas), `pydantic` (para validación y modelado de datos).

## Requisitos Previos

Para ejecutar este proyecto, se necesita:

1. **Docker Desktop**
2.  **Docker Compose**

## Configuración y Ejecución del Servicio

Pasos para levantar el contenedor de la API en tu máquina local.

### 1. Navegar al Directorio del Backend

Tras clonar el repositorio, abre tu terminal y navega a la carpeta raíz del proyecto Backend (`sportclub-api/`):

```bash
cd sportclub-api
```

### 2. Levantar la Instancia del Backend

Utiliza `docker compose` para construir la imagen del contenedor y ejecutar el servicio en segundo plano

```bash
docker compose up -d
```

### 3. Acceso a la API

Una vez que el contenedor esté activo, la API estará disponible en `http://localhost:8000`.

- Documentación interactiva: `http://localhost:8000/docs`
- Endpoint de Beneficios: `http://localhost:8000/api/v1/beneficios`
- Endpoint de Beneficio: `http://localhost:8000/api/v1/beneficios/{id}`
