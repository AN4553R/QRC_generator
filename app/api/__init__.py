from flask import Blueprint
from app.api import errors

bp = Blueprint('api', __name__)

from app.api import qr
