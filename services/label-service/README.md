# label Service - Endpoints

## 🌐 Endpoints

### 1. Health Check

```
GET /health
```

**Descripción:** Verifica que el servicio esté corriendo.

**Respuesta de ejemplo:**

```json
{
  "service": "label-service",
  "status": "healthy"
}
```

---

### 2. Obtener etiquetas

```
GET /label
```

**Descripción:** Devuelve el stock actual de todos las etiquetas.

**Respuesta de ejemplo:**

```json
[
    { id: 1, "label": "LABEL-001", "desc": "Etiqueta para envíos nacionales", },
    { id: 2, "label": "LABEL-002", "desc": "Etiqueta para envíos internacionales", },    
    { id: 3, "label": "LABEL-003", "desc": "Etiqueta para envíos express", },
]
```

---

### 3. Crear etiqueta (acción principal)

```
POST /create label
```

**Descripción:** Creación de una nueva etiqueta.

**Payload:**

```json
{
  "label": "label-001",
  "desc" : "Etiqueta para envíos nacionales"
}
```

**Respuesta de ejemplo (éxito):**

```json
{
  "label": {
    {
      "created": true,
      "labelId": 4
    }
  }
}
```

**Respuesta de ejemplo (error simulado):**

```json
{
  "detail": "Error aleatorio al crear label"
}
```

---

### 4. Consultar etiqueta

```
POST /get_label
```

**Descripción:** Obtener una etiqueta existente.

**Payload:**

```json
{
  "id": 1
}
```

**Respuesta de ejemplo:**

```json
{
  "label": {
    "label": { id: 1, "label": "LABEL-001", "desc": "Etiqueta para envíos nacionales", },
    "ok": true,
  }
}
```
