import httpx
import logging
from typing import List, Dict, Any
from pydantic import ValidationError
from app.core.models import BeneficioSummary, BeneficioDetail # Se importan models de core
from app.infra.errors import SportclubAPIError, CorruptedDataError, BeneficioNotFoundError # Se importan clases de errores personalizadas

logger = logging.getLogger(__name__)


# Cliente HTTP

class SportclubClient:
    # URLs de la API externa
    BENEFICIOS_URL = "https://asociate-api-challenge.prod.sportclub.com.ar/api/beneficios"
    DETALLE_BASE_URL = "https://api-beneficios.prod.sportclub.com.ar/api/beneficios/"

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=10.0)


    async def get_beneficios_data(self) -> List[BeneficioSummary]:
        logger.info("Infra: Solicitando lista de beneficios a la API externa.")
        
        raw_data = await self.safe_get(self.BENEFICIOS_URL)

        if not isinstance(raw_data, List):
            logger.error("Infra: Datos recibidos mal formados (no es una lista).")
            raise CorruptedDataError("Datos recibidos corruptos: formato inesperado de la lista.")

        return self.validate_models(raw_data, BeneficioSummary)


    async def get_beneficio_detalle_data(self, beneficio_id: int) -> BeneficioDetail:
        url = f"{self.DETALLE_BASE_URL}{beneficio_id}"
        logger.info(f"Infra: Solicitando detalle para beneficio ID: {beneficio_id}")

        try:
            full_response = await self.safe_get(url)
        except BeneficioNotFoundError:
            raise

        raw_data = full_response.get("body")

        if not raw_data or not isinstance(raw_data, Dict):
            logger.error("Infra: Detalle de beneficio mal formado o campo 'body' ausente.")
            raise CorruptedDataError("Datos de detalle de beneficio mal formados: 'body' no encontrado.")
        
        return self.validate_models(raw_data, BeneficioDetail)


    async def safe_get(self, url: str) -> Any:
        try:
            response = await self.client.get(url)
            response.raise_for_status()

            return response.json()

        except httpx.TimeoutException as e:
            logger.error(f"Infra: Timeout consultando {url}: {e}")
            raise SportclubAPIError("API Externa: Tiempo de espera agotado.") from e

        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            logger.error(f"Infra: Error HTTP {status} consultando {url}")

            if status == httpx.codes.NOT_FOUND:
                raise BeneficioNotFoundError("API Externa: Recurso no encontrado.") from e
            else:
                raise SportclubAPIError(
                    f"API Externa: HTTP {status}", status_code=status
                ) from e

        except Exception as e:
            logger.error(f"Infra: Error inesperado consultando {url}: {e}", exc_info=True)
            raise SportclubAPIError("API Externa: Error inesperado.") from e


    def validate_models(self, data: Any, model: Any):
        try:
            if isinstance(data, List):
                return [model.model_validate(item) for item in data]
            else:
                return model.model_validate(data)

        except ValidationError as e:
            logger.error(f"Validación Pydantic fallida: {e}")
            raise CorruptedDataError(f"Validación fallida de detalle de beneficio: {e}") from e        