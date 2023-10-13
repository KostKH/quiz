from datetime import datetime
from uuid import UUID, uuid4

import aiohttp

from business_layer.schemas import Question
from config import settings
from db_layer import db_engine as db
from db_layer import models
from db_layer.crud import question_crud


async def get_questions(number: int, quiz_id: UUID) -> list[Question]:
    """Функция для обращения к внешнему API с вопросами викторины и
    валидации полученных данных через схему Questions."""
    url: str = settings.quiz_api_url.format(number)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
    questions = []
    for item in data:
        question = Question(
            question_id=item['id'],
            question=item['question'],
            correct_answer=item['answer'],
            quiz_id=quiz_id,
            add_date=datetime.now(),
        )
        questions.append(question)
    return questions[:number]


async def get_and_save_questions(
    question_number: int,
    session: db.AsyncSession
) -> list[models.Question]:
    """Функция инициирует отправку запросов к внешнему API для получения
    нужного количества вопросов викторины и сохраняет вопросы в базу.
    Возвращает список ORM-объектов."""
    question_list = []
    quiz_id = uuid4()
    while question_number > len(question_list):
        questions = await get_questions(
            number=question_number - len(question_list),
            quiz_id=quiz_id)
        saved_questions = await question_crud.create_all(questions, session)
        question_list.extend(saved_questions)
    return question_list
