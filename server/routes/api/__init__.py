from .crawl import router as crawl_router
from .login import router as login_router
from .menu import router as menu_router
from .payment import router as payment_router

routes = [
    crawl_router,
    login_router,
    menu_router,
    payment_router
]
