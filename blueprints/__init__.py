from .system import auth, payments, admin
from .client import personal, modals, files


Blueprints = [
    auth.b,
    personal.b,
    payments.b,
    modals.b,
    files.b,
    admin.b
]