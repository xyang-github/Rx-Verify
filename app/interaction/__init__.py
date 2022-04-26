from flask import Blueprint

interaction = Blueprint("interaction", __name__)

from . import views
