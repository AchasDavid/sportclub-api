# app/api/beneficios_controller.py

from fastapi import HTTPException, status
from app.infra.sportclub_client import SportclubClient
from app.infra.errors import (
    SportclubAPIError,
    BeneficioNotFoundError,
    CorruptedDataError
)

client = SportclubClient()


async def get_beneficios_controller():
    try:
        beneficios = await client.get_beneficios_data()
        return beneficios
    except CorruptedDataError | SportclubAPIError as e:
        raise HTTPException(
            status_code = getattr(e, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR),
            detail = f"Ocurrió un error al procesar la solicitud: {e}"
        )

async def get_beneficio_detalle_controller(beneficio_id: int):
    try:
        detalle = await client.get_beneficio_detalle_data(beneficio_id)
        return detalle
    except BeneficioNotFoundError | CorruptedDataError | SportclubAPIError as e:
        raise HTTPException(
            status_code = getattr(e, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR),
            detail = f"Ocurrió un error al procesar la solicitud: {e}"
        )