import datetime as dt
from uuid import UUID

from pydantic import BaseModel


class Question(BaseModel):
    """Схема, используемая при создании вопроса"""

    question_id: int
    question: str
    correct_answer: str
    answer: str | None = None
    quiz_id: UUID
    add_date: dt.datetime

    class Config:
        from_attributes = True


class InitiateQuiz(BaseModel):
    """Схема, используемая для старта викторины"""

    questions_num: int


class Quiz(BaseModel):
    """Схема для отправки ответа на вопрос и следующего вопроса
    участнику викторины."""

    quiz_id: UUID
    previous_question_correct_answer: str | None = None
    question_id: int | None = None
    question: str | None = None


class QuizAnswer(BaseModel):
    """Схема, для отправки участником викторины ответа на вопрос."""

    quiz_id: UUID
    question_id: int
    answer: str


class NotFound(BaseModel):
    """Схема для сообщения об остутствии данных в БД."""

    detail: str = 'Запрошенные данные не найдены.'
