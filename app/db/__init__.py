from flask import Blueprint

db = Blueprint("db", __name__)

from . import database_queries
