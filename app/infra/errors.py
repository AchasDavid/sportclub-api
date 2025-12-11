import httpx

# Clases de Errores Personalizadas

class SportclubAPIError(Exception):
    # Excepción base para errores de la API externa (caída, timeout, error 500)
    def __init__(self, message: str, status_code: int = 503): # Por defecto 503 Service Unavailable
        super().__init__(message)
        self.status_code = status_code

class CorruptedDataError(Exception):
    # Excepción específica para datos corruptos
    def __init__(self, message: str):
        super().__init__(message)
        self.satus_code = httpx.codes.BAD_GATEWAY

class BeneficioNotFoundError(Exception):
    # Excepción específica para el error 404 de beneficio no encontrado
    def __init__(self, beneficio_id: int):
        super().__init__(f"Beneficio con ID {beneficio_id} no existe en la API externa.")
        self.status_code = httpx.codes.NOT_FOUND
