# services/transport-service/app/main.py
from flask import Flask, jsonify, request
import os, random

app = Flask(__name__)

# Variables de entorno
SERVICE_NAME = os.getenv("SERVICE_NAME", "transport-service")
SERVICE_PORT = int(os.getenv("SERVICE_PORT", 5005))

# Memoria simulada
assignments = {}

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": SERVICE_NAME}), 200

@app.route("/assign_carrier", methods=["POST"])
def assign_carrier():
    """Asigna un transportista a un pedido"""
    order = request.json
    order_id = order.get("orderId", f"ORD-{random.randint(1000,9999)}")
    carrier_id = f"CRR-{random.randint(10,99)}-FastShip"

    carrier_data = {
        "carrier": {
            "carrierId": carrier_id,
            "assigned": True
        }
    }

    assignments[order_id] = carrier_data
    return jsonify(carrier_data), 200

@app.route("/cancel_assignment", methods=["POST"])
def cancel_assignment():
    """Desasigna el transportista del pedido"""
    order = request.json
    order_id = order.get("orderId")

    if order_id in assignments:
        carrier_id = assignments[order_id]["carrier"]["carrierId"]
        assignments[order_id]["carrier"]["assigned"] = False
        assignments[order_id]["carrier"]["status"] = "CANCELLED"
    else:
        carrier_id = "UNKNOWN"

    return jsonify({
        "status": "cancelled",
        "carrierId": carrier_id,
        "orderId": order_id
    }), 200

@app.route("/assignments", methods=["GET"])
def list_assignments():
    """Lista todas las asignaciones almacenadas"""
    return jsonify(assignments), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=SERVICE_PORT)
