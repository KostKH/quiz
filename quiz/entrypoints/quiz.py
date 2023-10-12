"""Роутеры для едпойнтов викторины."""
import logging
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from business_layer import schemas
from business_layer.question_retrieval import get_and_save_questions
from db_layer import db_engine as db
from db_layer.crud import question_crud

router = APIRouter()


@router.post(
    path='/',
    summary='Начать викторину',
    status_code=status.HTTP_200_OK,
    response_model=schemas.Quiz,
    response_model_exclude_none=True,
)
async def start_quiz(
    input: schemas.InitiateQuiz,
    session: Annotated[db.AsyncSession, Depends(db.get_async_session)],
) -> schemas.Quiz:
    try:
        questions = await get_and_save_questions(input.questions_num, session)
        await session.refresh(questions[0])
        return schemas.Quiz(
            quiz_id=questions[0].quiz_id,
            question_id=questions[0].question_id,
            question=questions[0].question)
    except Exception as e:
        logging.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка сервиса.')


@router.post(
    path='/answer',
    summary='Отправить ответ на вопрос',
    response_model=schemas.Quiz,
    response_model_exclude_none=True,
    responses={404: {'model': schemas.NotFound}},)
async def post_answer(
    input: schemas.QuizAnswer,
    session: Annotated[db.AsyncSession, Depends(db.get_async_session)],
) -> schemas.Quiz:
    question = await question_crud.update_question(input, session)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=('Неправильный номер вопроса/номер викторины, '
                    'либо ответ на вопрос уже был дан')
        )
    correct_answer = question.correct_answer
    next_question = await question_crud.get_next_quiz_question(
        quiz_id=input.quiz_id,
        session=session)
    try:
        return schemas.Quiz(
            quiz_id=input.quiz_id,
            previous_question_correct_answer=correct_answer,
            question_id=next_question.question_id if next_question else None,
            question=next_question.question if next_question else None)
    except Exception as e:
        logging.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка сервиса.')


@router.get(
    path='/next_question/{quiz_id}',
    summary='Получить следующий вопрос',
    response_model=schemas.Quiz,
    response_model_exclude_none=True,
    responses={
        404: {'model': schemas.NotFound},
    },
)
async def get_next_question(
    quiz_id: UUID,
    session: Annotated[db.AsyncSession, Depends(db.get_async_session)],
) -> schemas.Quiz:
    question = await question_crud.get_next_quiz_question(quiz_id, session)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Вопрос не найден.')
    return schemas.Quiz(
        quiz_id=quiz_id,
        question_id=question.question_id,
        question=question.question,
    )
