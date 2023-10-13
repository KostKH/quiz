import datetime as dt
from uuid import UUID

from pydantic import BaseModel, Field


class Question(BaseModel):
    """Схема, используемая при создании вопроса"""

    question_id: int = Field(
        gt=0,
        description='ID вопроса должен быть больше 0')
    question: str = Field(description='Текст вопроса', max_length=255)
    correct_answer: str = Field(
        description='Правильный ответ',
        max_length=255)
    answer: str | None = Field(
        default=None,
        description='Текст вопроса',
        max_length=255)
    quiz_id: UUID
    add_date: dt.datetime

    class Config:
        from_attributes = True


class InitiateQuiz(BaseModel):
    """Схема, используемая для старта викторины"""

    questions_num: int = Field(
        gt=0,
        le=100,
        description='Количество вопросов, должно быть больше 0')

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'questions_num': 5,
                }
            ]
        }
    }


class QuizResponseNoAnswer(BaseModel):
    """Схема для отправки следующего вопроса
    участнику викторины."""

    quiz_id: UUID = Field(description='Номер (UUID) викторины')
    question_id: int | None = Field(
        default=None,
        gt=0,
        description='ID вопроса, должен быть больше 0')
    question: str | None = Field(
        default=None,
        description='Текст вопроса',
        max_length=255)

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'quiz_id': 'a038f339-2c66-4565-90e8-8507da656fa0',
                    'question_id': 2345,
                    'question': 'Текст следующего вопроса',
                }
            ]
        }
    }


class QuizResponseFull(QuizResponseNoAnswer):
    """Схема для отправки ответа на вопрос и следующего вопроса
    участнику викторины."""

    previous_question_correct_answer: str | None = Field(
        default=None,
        description='Правильный ответ на предыдущий вопрос',
        max_length=255)

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'quiz_id': 'a038f339-2c66-4565-90e8-8507da656fa0',
                    'previous_question_correct_answer': (
                        'Правильный ответ на предыдущий вопрос'),
                    'question_id': 2345,
                    'question': 'Текст следующего вопроса',
                }
            ]
        }
    }


class QuizAnswer(BaseModel):
    """Схема, для отправки участником викторины ответа на вопрос."""

    quiz_id: UUID = Field(description='Номер (UUID) викторины')
    question_id: int = Field(
        gt=0,
        description='ID вопроса, должен быть больше 0')
    answer: str = Field(
        description='Ответ на вопрос',
        max_length=255)

    model_config = {
        'json_schema_extra': {
            'examples': [
                {
                    'quiz_id': 'a038f339-2c66-4565-90e8-8507da656fa0',
                    'question_id': 12458,
                    'answer': 'Ответ',
                }
            ]
        }
    }


class NotFound(BaseModel):
    """Схема для сообщения об остутствии данных в БД."""

    detail: str = 'Запрошенные данные не найдены.'
