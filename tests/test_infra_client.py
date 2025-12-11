import pytest
import respx
import httpx
from typing import List
from app.infra.sportclub_client import SportclubClient, BeneficioNotFoundError
from app.core.models import BeneficioSummary, BeneficioDetail

# Datos simulados de la API de Sportclub
MOCK_BENEFICIO_LIST = [
    {
        "id": 1,
        "comercio": "WALMART",
        "descripcion": "Descuento del 10% en electrónicos",
        "aclaracion": "Solo en tiendas físicas",
        "tarjeta": True,
        "efectivo": False,
        "vencimiento": "2026-01-21T00:00:00",
        "categoria": "TECNOLOGIA",
        "imagenUrl": "https://url.com/imagen.jpg"
    },
    {
        "id": 2,
        "comercio": "QUILMES",
        "descripcion": "2x1 en pintas",
        "aclaracion": None,
        "tarjeta": False,
        "efectivo": True,
        "vencimiento": "2023-01-01T00:00:00", # Vencido
        "categoria": "BEBIDAS",
        "imagenUrl": "https://url.com/cerveza.jpg"
    }
]

MOCK_BENEFICIO_DETAIL_BODY = {
    "id": 8,
    "comercio": "QUIKSILVER",
    "descripcion": "Indumentaria unisex.",
    "aclaratoria": "No acumulable con otras promociones.",
    "descuento": 15,
    "tarjeta": False,
    "efectivo": True,
    "orden": None,
    "esFavorito": False,
    "esNuevo": None,
    "ordenNuevo": None,
    "vencimiento": None,
    "puntuacion": 5,
    "archivado": False,
    "ultimaActualizacion": "2024-01-11T18:36:52.928Z",
    "informadorId": 17,
    "visitas": 2596,
    "payclub": False,
    "payclubDescuentoDesc": None,
    "payclubDescuento": 0,
    "CategoriaGeneralId": 2,
    "CategoriaSimpleId": 20,
    "CategoriaGeneral": {"id": 2, "nombre": "moda", "archivado": False, "orden": 2},
    "CategoriaSimple": {"id": 20, "nombre": "indumentaria-unisex", "archivado": False, "CategoriaGeneralId": 2},
    "Imagens": [{"id": 12, "url": "https://url.com/img1.webp", "BeneficioId": 8, "CategoriaGeneralId": None, "CategoriaSimpleId": None}],
    "Dium": {"id": 5439, "lunes": True, "martes": True, "miercoles": True, "jueves": True, "viernes": True, "sabado": True, "domingo": True, "feriados": True, "BeneficioId": 8},
    "Contacto": {"id": 12, "nombre": "test", "apellido": "test", "telefono": "123456789", "email": "aa@aa.com", "instagram": "", "BeneficioId": 8},
    "Sucursals": []
}

MOCK_BENEFICIO_DETAIL_RESPONSE = {
    "error": False,
    "status": 200,
    "body": MOCK_BENEFICIO_DETAIL_BODY
}

client = SportclubClient()

@pytest.mark.asyncio
@respx.mock
async def test_get_beneficios_success(respx_mock):
    """Prueba que la lista de beneficios se consume y valida correctamente."""
    respx_mock.get(client.BENEFICIOS_URL).return_value = httpx.Response(200, json=MOCK_BENEFICIO_LIST)

    beneficios = await client.get_beneficios_data()

    assert len(beneficios) == 2
    assert isinstance(beneficios, List)
    assert isinstance(beneficios[0], BeneficioSummary)
    assert beneficios[0].comercio == "WALMART"
    assert beneficios[1].comercio == "QUILMES"


@pytest.mark.asyncio
@respx.mock
async def test_get_beneficio_detalle_success(respx_mock):
    """Prueba que el detalle del beneficio se consume y se extrae del 'body'."""
    url = f"{client.DETALLE_BASE_URL}8"
    respx_mock.get(url).return_value = httpx.Response(200, json=MOCK_BENEFICIO_DETAIL_RESPONSE)

    detalle = await client.get_beneficio_detalle_data(beneficio_id=8)

    assert isinstance(detalle, BeneficioDetail)
    assert detalle.comercio == "QUIKSILVER"
    assert detalle.CategoriaGeneral.nombre == "moda"
    assert detalle.es_favorito == False


@pytest.mark.asyncio
@respx.mock
async def test_get_beneficio_detalle_404(respx_mock):
    """Prueba que un 404 de la API externa lanza BeneficioNotFoundError."""
    url = f"{client.DETALLE_BASE_URL}999"
    respx_mock.get(url).return_value = httpx.Response(404)

    with pytest.raises(BeneficioNotFoundError) as exc_info:
        await client.get_beneficio_detalle_data(beneficio_id=999)
    
    assert "no existe en la API externa" in str(exc_info.value)
    assert exc_info.value.status_code == 404


def test_beneficio_activo_logic():
    """Prueba que la propiedad 'activo' calcula el estado correctamente."""
    
    activo_data = MOCK_BENEFICIO_LIST[0]
    beneficio_activo = BeneficioSummary.model_validate(activo_data)
    
    inactivo_data = MOCK_BENEFICIO_LIST[1]
    beneficio_inactivo = BeneficioSummary.model_validate(inactivo_data)
    
    sin_vencimiento_data = MOCK_BENEFICIO_LIST[0].copy()
    sin_vencimiento_data['vencimiento'] = None
    beneficio_sin_vencimiento = BeneficioSummary.model_validate(sin_vencimiento_data)

    assert beneficio_activo.activo is True
    assert beneficio_inactivo.activo is False
    assert beneficio_sin_vencimiento.activo is True