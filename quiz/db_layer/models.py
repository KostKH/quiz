from sqlalchemy import DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column

from .db_engine import Base


class Question(Base):
    """Модель Алхимии к таблице question в БД."""
    question_id = mapped_column(Integer, primary_key=True)
    question = mapped_column(String(255), nullable=False)
    correct_answer = mapped_column(String(255), nullable=False)
    answer = mapped_column(String(255), nullable=True)
    quiz_id = mapped_column(UUID, nullable=False)
    add_date = mapped_column(DateTime, nullable=False)
