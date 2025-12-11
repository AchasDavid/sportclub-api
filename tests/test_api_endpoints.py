from fastapi.testclient import TestClient
import respx
import httpx

from app.main import app
from app.infra.sportclub_client import SportclubClient
from tests.test_infra_client import MOCK_BENEFICIO_LIST, MOCK_BENEFICIO_DETAIL_RESPONSE

client = TestClient(app)

@respx.mock
def test_get_beneficios_endpoint_success(respx_mock):
    """Prueba el endpoint /api/v1/beneficios en caso de éxito."""
    # Mocking de la API externa
    mock_url = SportclubClient.BENEFICIOS_URL
    respx_mock.get(mock_url).return_value = httpx.Response(200, json=MOCK_BENEFICIO_LIST)

    # Llamada al endpoint de FastAPI
    response = client.get("/api/v1/beneficios")

    # Asersiones
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]['comercio'] == "WALMART"
