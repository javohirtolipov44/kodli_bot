from aiogram import Router
from . import chanel, checksub, deep_link, admin

router = Router()
router.include_router(admin.router)
router.include_router(deep_link.router)
router.include_router(checksub.router)
router.include_router(chanel.router)

