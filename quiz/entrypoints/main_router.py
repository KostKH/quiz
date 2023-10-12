"""Подключение всех роутеров к главному роутеру."""
from fastapi import APIRouter

from . import quiz

main_router = APIRouter(prefix='/api/v1')

main_router.include_router(
    router=quiz.router,
    prefix='/quiz',
    tags=['Quiz'],
)
