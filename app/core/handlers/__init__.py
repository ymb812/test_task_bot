from core.handlers.welcome import router as welcome_router
from core.handlers.basic import router as basic_router
from core.handlers.admin import router as admin_router
from core.handlers.faq import router as rules_router


routers = [welcome_router, basic_router, admin_router, rules_router]
