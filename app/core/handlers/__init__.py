from core.handlers.registration import router as registration_router
from core.handlers.basic import router as basic_router
from core.handlers.admin import router as admin_router
from core.handlers.faq import router as rules_router
from core.handlers.wrong_input import router as error_router


routers = [registration_router, basic_router, admin_router, rules_router, error_router]
