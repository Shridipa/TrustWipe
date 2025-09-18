from flask import Blueprint, request, jsonify
from local_verifier.verify import verify_certificate

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/verify', methods=['POST'])
def api_verify():
    cert = request.get_json()
    try:
        result = verify_certificate(cert)
        return jsonify({"status": "success", "result": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400