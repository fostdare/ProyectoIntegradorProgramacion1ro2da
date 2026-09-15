from pydantic import BaseModel, Field
from typing import Optional


class TareaCreate(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=200)
    descripcion: str = Field(..., min_length=1)
    prioridad: int = Field(..., ge=1, le=3)
    categoria: str = Field(..., min_length=1, max_length=100)
    responsable: str = Field(..., min_length=1, max_length=100)
    fecha_limite: str = Field(..., min_length=8, max_length=10)


class TareaUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=1, max_length=200)
    descripcion: Optional[str] = None
    prioridad: Optional[int] = Field(None, ge=1, le=3)
    categoria: Optional[str] = Field(None, min_length=1, max_length=100)
    responsable: Optional[str] = Field(None, min_length=1, max_length=100)
    fecha_limite: Optional[str] = Field(None, min_length=8, max_length=10)
    estado: Optional[str] = None


class TareaResponse(BaseModel):
    id: int
    titulo: str
    descripcion: str
    prioridad: int
    estado: str
    categoria: str
    responsable: str
    fecha_limite: str

    class Config:
        from_attributes = True


class EstadisticasResponse(BaseModel):
    total_tareas: int
    pendientes: int
    en_curso: int
    finalizadas: int
    porcentaje_completadas: float


class MensajeResponse(BaseModel):
    mensaje: str
