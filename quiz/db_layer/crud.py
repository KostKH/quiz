from sqlalchemy import null, select, update
from sqlalchemy.dialects.postgresql import insert as postgres_upsert

from business_layer import schemas
from db_layer import db_engine
from db_layer.models import Question


class QuestionCRUD():
    """Класс с операциями CRUD для модели Question."""

    async def get(
        self,
        obj_id: int,
        session: db_engine.AsyncSession
    ) -> Question | None:
        """Метод получает из БД запись вопроса
        по первичному ключу:`question_id`."""
        return await session.get(Question, obj_id)

    async def get_next_quiz_question(
        self,
        quiz_id: str,
        session: db_engine.AsyncSession,
    ) -> Question | None:
        """Метод возвращает следующий вопрос в рамках данного uuid викторины,
        на который участник ещё не давал ответ."""
        query = (select(Question)
                 .where(Question.quiz_id == quiz_id)
                 .where(Question.answer == null()))
        return await session.scalar(query.limit(1))

    async def create_all(
        self,
        questions: list[schemas.Question],
        session: db_engine.AsyncSession,
    ) -> list[Question]:
        """Метод создаёт в БД переданные записи вопросов."""
        question_dicts = [item.dict() for item in questions]
        query = (postgres_upsert(Question)
                 .values(question_dicts)
                 .on_conflict_do_nothing(index_elements=['question_id'])
                 .returning(Question))
        results = await session.scalars(
            query,
            execution_options={"populate_existing": True}
        )
        await session.commit()
        return results.all()

    async def update_question(
        self,
        data: schemas.QuizAnswer,
        session: db_engine.AsyncSession,
    ) -> Question | None:
        """Метод обновляет в БД запись вопроса: записывает ответ на него.
        Ответ записывается только если до этого поле было пустым. То есть
        допускается только однократное сохранение ответа."""
        stmt = (update(Question)
                .where(Question.question_id == data.question_id)
                .where(Question.quiz_id == data.quiz_id)
                .where(Question.answer == null())
                .values(answer=data.answer)
                .returning(Question))
        results = await session.scalars(stmt)
        await session.commit()
        try:
            result = next(results)
            await session.refresh(result)
            return result
        except StopIteration:
            return None


question_crud = QuestionCRUD()
