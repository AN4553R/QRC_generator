from flask import send_file, request
from app import db
from app.api import bp
from app.api.errors import bad_request
from app.models import User
import qrcode


@bp.route("/", methods=['GET'])
def index():
    return "Welcome to QR Generator API!"


@bp.route('/user', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'firstname' not in data or 'lastname' not in data or 'email' not in data:
        return bad_request('must include firstname, lastname and email fields')
    if not User.query.filter_by(email=data['email']).first():
        user = User(firstname=data['firstname'], lastname=data['lastname'], email=data['email'])
        db.session.add(user)
        db.session.commit()
    user = User.query.filter_by(email=data['email']).first()
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(user.id)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    img.save("app/qrs/user%s.png" % user.id)
    try:
        result = send_file("qrs/user%s.png" % user.id, mimetype='image/png')
    except FileNotFoundError:
        return bad_request("QR code not found")
    return result


@bp.route("/form", methods=['POST'])
def receive_message():
    data = request.get_json() or {}
    if 'id' not in data or 'message' not in data:
        return bad_request('must include id and message fields')
    return str(User.query.filter_by(email=data['email']).first())
