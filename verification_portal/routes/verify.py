from flask import Blueprint, request, render_template
import json
from local_verifier.verify import verify_certificate

verify_bp = Blueprint('verify', __name__)

@verify_bp.route('/verify', methods=['POST'])
def verify():
    cert_data = request.form.get('certificate_json')
    try:
        cert = json.loads(cert_data)
        result = verify_certificate(cert)
        return render_template('result.html', result=result)
    except Exception as e:
        return render_template('error.html', message=str(e))