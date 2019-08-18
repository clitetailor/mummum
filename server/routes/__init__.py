from flask import Blueprint

from .api import routes

from .auth import router as auth_router
from .index import router as index_router
from .menu import router as menu_router
from .payment import router as payment_router
from .summary import router as summary_router
from .total_debt import router as total_debt_router
from .week_summary import router as week_summary_router

routes = routes + [
    auth_router,
    index_router,
    menu_router,
    payment_router,
    summary_router,
    total_debt_router,
    week_summary_router
]
