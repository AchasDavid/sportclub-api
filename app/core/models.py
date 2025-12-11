from pydantic import BaseModel, Field, AliasChoices
from typing import Optional, List, Any
from datetime import datetime, timedelta, timezone

# Modelos anidados del detalle de un beneficio

class CategoriaGeneralModel(BaseModel):
    id: int = Field(..., description='Id de categoría general')
    nombre: str = Field(..., description='Nombre de la categoría general')
    archivado: bool = Field(..., description='Indica si la categoría general está archivada')
    orden: Optional[int] = Field(None, description='Orden de presentación')

class CategoriaSimpleModel(BaseModel):
    id: int = Field(..., description='Id de categoría simple')
    nombre: str = Field(..., description='Nombre de la categoría simple')
    archivado: bool = Field(..., description='Indica si la categoría simple está archivada')
    CategoriaGeneralId: int = Field(..., description='Id de la categoría general relacionada')

class ImagenModel(BaseModel):
    id: int = Field(..., description='Id de imagen')
    url: str = Field(..., description='URL de imagen')
    BeneficioId: int = Field(..., description='Id de beneficio relacionado')
    CategoriaGeneralId: Optional[int] = Field(None, description='Id de categoría general relacionada')
    CategoriaSimpleId: Optional[int] = Field(None, description='Id de categoría simple relacionada')

class DiumModel(BaseModel):
    id: int
    lunes: bool
    martes: bool
    miercoles: bool
    jueves: bool
    viernes: bool
    sabado: bool
    domingo: bool
    feriados: bool
    BeneficioId: int

class ContactoModel(BaseModel):
    id: int = Field(..., description='Id de contacto')
    nombre: Optional[str] = Field(None, description='Nombre del contacto')
    apellido: Optional[str] = Field(None, description='Apellido del contacto')
    telefono: Optional[str] = Field(None, description='Teléfono del contacto')
    email: Optional[str] = Field(None, description='Email del contacto')
    instagram: Optional[str] = Field(None, description='Usuario de instagram de contacto')
    BeneficioId: int = Field(..., description='Id de beneficio relacionado')


# Modelo de beneficio listado (GET /beneficios)

class BeneficioSummary(BaseModel):
    id: int
    comercio: str = Field(..., description="Nombre del comercio.")
    descripcion: str = Field(..., description="Descripción breve del beneficio.")
    aclaracion: Optional[str] = Field(None, description="Aclaraciones o restricciones.")
    tarjeta: bool = Field(False, description="Indica si aplica con tarjeta.")
    efectivo: bool = Field(False, description="Indica si aplica en efectivo.")    
    vencimiento: Optional[datetime] = Field(None, description="Fecha de vencimiento.")
    categoria: Optional[str] = Field(None, description="Categoría principal.")    
    imagenUrl: Optional[str] = Field(None, description="URL de la imagen principal del beneficio.")
    
    class ConfigDict:
        from_attributes = True 
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
    @property
    def activo(self) -> bool:
        # Se determina si un beneficio está activo o no basándose en su fecha de vencimiento

        ba_tz = timezone(timedelta(hours=-3))
        now = datetime.now(ba_tz)
        
        if self.vencimiento is None:
            return True
        
        if self.vencimiento.tzinfo is None:
             vencimiento_tz = self.vencimiento.replace(tzinfo=ba_tz)
        else:
             vencimiento_tz = self.vencimiento
             
        return vencimiento_tz > now        


# Modelos de Detalle (GET /beneficios/:id)

class BeneficioDetail(BaseModel):

    id: int = Field(..., description="Id del beneficio")
    comercio: str = Field(..., description="Nombre del comercio.")
    descripcion: str = Field(..., description="Descripción breve del beneficio.")
    aclaratoria: Optional[str] = Field(None, description="Aclaraciones o restricciones")
    descuento: Optional[int] = Field(None, description="Descuento del beneficio")
    tarjeta: bool = Field(False, description="Indica si aplica con tarjeta.")
    efectivo: bool = Field(False, description="Indica si aplica en efectivo.")
    orden: Optional[int] = Field(None, description="Orden de presentación")
    
    es_favorito: bool = Field(False, validation_alias=AliasChoices('esFavorito', 'es_favorito'))
    es_nuevo: Optional[bool] = Field(None, validation_alias=AliasChoices('esNuevo', 'es_nuevo'))
    orden_nuevo: Optional[int] = Field(None, validation_alias=AliasChoices('ordenNuevo', 'orden_nuevo'))
    vencimiento: Optional[datetime] = Field(None, description="Fecha de vencimiento.")
    ultima_actualizacion: Optional[datetime] = Field(
        None, 
        validation_alias=AliasChoices('ultimaActualizacion', 'ultima_actualizacion')
    )
    informador_id: Optional[int] = Field(None, validation_alias=AliasChoices('informadorId', 'informador_id'))
    payclub_descuento_desc: Optional[str] = Field(None, validation_alias=AliasChoices('payclubDescuentoDesc', 'payclub_descuento_desc'))
    payclub_descuento: Optional[int] = Field(None, validation_alias=AliasChoices('payclubDescuento', 'payclub_descuento'))
    puntuacion: Optional[int] = None
    archivado: bool = False
    visitas: Optional[int] = None
    payclub: bool = False
    
    CategoriaGeneralId: int 
    CategoriaSimpleId: int
    
    # Modelos anidados
    CategoriaGeneral: CategoriaGeneralModel
    CategoriaSimple: CategoriaSimpleModel
    Imagens: List[ImagenModel] = Field(default_factory=list)
    Dium: DiumModel
    Contacto: ContactoModel
    Sucursals: List[Any] = Field(default_factory=list)