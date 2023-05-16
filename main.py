from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier origen
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todas las cabeceras
)

class DatosUsuario(BaseModel):
    usuario: str
    contra: str
    correcto: int
    pregunta: str
    pregunta_correcta: int

datos_dict = {}  # Diccionario para almacenar los datos

@app.post("/datos")
def agregar_datos(datos: DatosUsuario):
    datos_dict[datos.usuario] = datos.dict()
    return {"mensaje": "Datos agregados exitosamente"}

@app.get("/datos/{usuario}")
def obtener_datos(usuario: str):
    if usuario in datos_dict:
        return datos_dict[usuario]
    return {"mensaje": "Usuario no encontrado"}

@app.put("/datos/{id}")
def actualizar_datos(usuario: str, datos: DatosUsuario):
    if usuario in datos_dict:
        datos_actualizados = datos.dict(exclude_unset=True)
        datos_dict[usuario].update(datos_actualizados)
        return {"mensaje": "Datos actualizados exitosamente"}
    return {"mensaje": "Usuario no encontrado"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8100)