from fastapi import APIRouter
from typing import List

from app.core.models import BeneficioSummary, BeneficioDetail
from app.api.controller import (
    get_beneficios_controller,
    get_beneficio_detalle_controller
)

router = APIRouter()


@router.get(
    "/beneficios",
    response_model=List[BeneficioSummary],
    summary="Obtiene la lista de beneficios desde Sportclub API"
)
async def get_beneficios():
    return await get_beneficios_controller()


@router.get(
    "/beneficios/{beneficio_id}",
    response_model=BeneficioDetail,
    summary="Obtiene los detalles de un beneficio por ID"
)
async def get_beneficio_detalle(beneficio_id: int):
    return await get_beneficio_detalle_controller(beneficio_id)
