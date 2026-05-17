"""
web.py — Interface Web (Flask) do Dog Walker Control.

Execute com:
    python -m src.web

A aplicação estará disponível em http://localhost:5000
"""

import os
from flask import Flask, render_template, request, jsonify
from src.core import DogWalkerControl

# Define os caminhos corretos para templates e static
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

# Inicializa a aplicação Flask
app = Flask(
    __name__,
    template_folder=TEMPLATES_DIR,
    static_folder=STATIC_DIR
)

# Instância global do controle de passeios
control = DogWalkerControl()


# ── ROTAS HTML ────────────────────────────────────────────────────────


@app.route("/")
def index():
    """Renderiza a página principal."""
    return render_template("index.html")


# ── ROTAS API REST ────────────────────────────────────────────────────


@app.route("/api/walks", methods=["GET"])
def api_get_walks():
    """Lista todos os passeios registrados."""
    try:
        walks = control.list_walks()
        return jsonify({"success": True, "data": walks}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/walks", methods=["POST"])
def api_add_walk():
    """Registra um novo passeio."""
    try:
        data = request.get_json()
        
        dog_name = data.get("dog_name", "").strip()
        owner_name = data.get("owner_name", "").strip()
        walks_per_day = data.get("walks_per_day", 1)
        days_of_week = data.get("days_of_week", [])
        phone = data.get("phone", "").strip()
        
        record = control.add_walk(dog_name, owner_name, walks_per_day, days_of_week, phone)
        return jsonify({"success": True, "data": record}), 201
    except ValueError as e:
        return jsonify({"success": False, "error": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/walks/<dog_name>", methods=["DELETE"])
def api_remove_walk(dog_name):
    """Remove um passeio pelo nome do cachorro."""
    try:
        removed = control.remove_walk(dog_name)
        if removed:
            return jsonify({"success": True, "message": f"Passeio de '{dog_name}' removido."}), 200
        else:
            return jsonify({"success": False, "error": f"Cachorro '{dog_name}' não encontrado."}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/total", methods=["GET"])
def api_total_revenue():
    """Retorna o valor total a receber no mês."""
    try:
        total = control.total_revenue()
        return jsonify({"success": True, "total": total}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/owner/<owner_name>", methods=["GET"])
def api_find_by_owner(owner_name):
    """Busca passeios por nome do dono."""
    try:
        results = control.find_by_owner(owner_name)
        return jsonify({"success": True, "data": results}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/schedule", methods=["GET"])
def api_schedule():
    """Retorna passeios agrupados por dia da semana."""
    try:
        schedule = control.walks_by_day()
        return jsonify({"success": True, "data": schedule}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/config", methods=["GET"])
def api_config():
    """Retorna configurações da aplicação (dias, preço, etc)."""
    from src.core import DAYS_OF_WEEK, MAX_DAYS, PRICE_PER_WALK
    return jsonify({
        "days_of_week": DAYS_OF_WEEK,
        "max_days": MAX_DAYS,
        "price_per_walk": PRICE_PER_WALK
    }), 200


# ── TRATAMENTO DE ERROS ────────────────────────────────────────────


@app.errorhandler(404)
def not_found(error):
    """Trata erros 404."""
    return jsonify({"success": False, "error": "Recurso não encontrado"}), 404


@app.errorhandler(500)
def server_error(error):
    """Trata erros 500."""
    return jsonify({"success": False, "error": "Erro interno do servidor"}), 500


# ── INICIALIZAÇÃO ──────────────────────────────────────────────────


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("  🐾 DOG WALKER CONTROL - SERVIDOR WEB 🐾")
    print("=" * 50)
    print("\n🌐 Acesse: http://localhost:5000")
    print("🛑 Pressione Ctrl+C para parar o servidor\n")
    app.run(debug=True, port=5000)
