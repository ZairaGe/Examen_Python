from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

# Importaciones locales
from . import models, auth, database

app = FastAPI(title="API de Gestión de Incidencias")

# --- ESQUEMAS PYDANTIC (Para validación de datos) ---
class IncidenciaBase(BaseModel):
    titulo: str
    descripcion: str
    prioridad: str
    estado: str

class IncidenciaResponse(IncidenciaBase):
    id: int
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

# --- ENDPOINTS ---

# 1. Login para obtener el Token (Público)
@app.post("/login")
def login(request: LoginRequest):
    if request.username == auth.USER_FIXED["username"] and request.password == auth.USER_FIXED["password"]:
        token = auth.create_access_token(data={"sub": request.username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Credenciales incorrectas")

# 2. Listado de incidencias (Público)
@app.get("/incidencias", response_model=List[IncidenciaResponse])
def get_incidencias(db: Session = Depends(database.get_db)):
    return db.query(models.Incidencia).all()

# 3. Crear incidencia (PROTEGIDO)
@app.post("/incidencias", response_model=IncidenciaResponse)
def create_incidencia(
    incidencia: IncidenciaBase, 
    db: Session = Depends(database.get_db), 
    current_user: str = Depends(auth.get_current_user)
):
    nueva_incidencia = models.Incidencia(**incidencia.model_dump())
    db.add(nueva_incidencia)
    db.commit()
    db.refresh(nueva_incidencia)
    return nueva_incidencia

# 4. Obtener info del usuario actual (PROTEGIDO)
@app.get("/me")
def read_users_me(current_user: str = Depends(auth.get_current_user)):
    return {"usuario_autenticado": current_user}