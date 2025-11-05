from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import os
import random

app = FastAPI(
    title="Label Service",
    description="Servicio para gestionar inventario como parte de la SAGA."
)

# --- Variables de Entorno ---
SERVICE_NAME = os.getenv("SERVICE_NAME", "label-service")
SERVICE_PORT = int(os.getenv("SERVICE_PORT", 5007))
FAILURE_RATE = float(os.getenv("FAILURE_RATE", 0.4))  # 30% de fallos

# --- Inventario simulado (en memoria) ---
# { "label-123": id }
label_db = [
    { id: 1, "label": "LABEL-001", "desc": "Etiqueta para envíos nacionales", },
    { id: 2, "label": "LABEL-002", "desc": "Etiqueta para envíos internacionales", },    
    { id: 3, "label": "LABEL-003", "desc": "Etiqueta para envíos express", },
]

def should_fail():
    return random.random() < FAILURE_RATE

@app.post("/create_label")
async def create_label(request: Request):
    """
    Creación de una nueva etiqueta.
    """

    saga_data = await request.json()

    data = await request.json()
    request_data = saga_data.get("request_data", {})
    label = request_data.get("label")
    desc = request_data.get("desc")
    if not label:
        raise HTTPException(status_code=400, detail="Falta 'label' en la SAGA")
    if should_fail():
        raise HTTPException(status_code=500, detail="Error aleatorio al crear label")
    label_id = len(label_db) + 1
    label_db.append({ "id": label_id, "label": label, "desc": desc })
    return JSONResponse({
        "label": {
            "created": True,
            "labelId": label_id
        }
    }, status_code=200)


@app.post("/get_label")
async def get_label(request: Request):
    """
    Obtener una etiqueta existente.
    """

    saga_data = await request.json()
    
    request_data = saga_data.get("request_data", {})
    id = request_data.get("id")

    if not id:
        raise HTTPException(status_code=400, detail="Falta 'id' en la SAGA")

    if id not in label_db:
        raise HTTPException(status_code=404, detail=f"Etiqueta {id} no encontrada")
    
    if should_fail():
        raise HTTPException(status_code=500, detail="Error aleatorio al crear label")
    label = label_db[id]

    return JSONResponse({
        "label": {
            "label": label,
            "ok": True,
        }
    }, status_code=200)

@app.get("/label")
async def get_label():
    """Endpoint para listar las etiquetas."""
    return JSONResponse(label_db)

@app.get("/health")
async def health():
    """Health check para Kubernetes."""
    return JSONResponse({"service": SERVICE_NAME, "status": "healthy"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=SERVICE_PORT)