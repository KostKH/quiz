import asyncio
import random
import sys
from contextlib import ExitStack
from datetime import datetime
from pathlib import Path
from uuid import UUID

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor

from business_layer import schemas
from config import settings
from db_layer.db_engine import get_async_session, sessionmanager
from db_layer.models import Question
from main import init_app

BASE_DIR = Path('.').absolute()

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield init_app(init_db=False)


@pytest.fixture
def client(app):
    with TestClient(app) as client:
        yield client


test_db = factories.postgresql_noproc(
    host=settings.db_hostname,
    port=settings.db_port,
    user=settings.db_user,
    dbname='test_db',
    password=settings.db_pass,
)


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
async def connection_test(test_db, event_loop):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password

    with DatabaseJanitor(
        pg_user, pg_host, pg_port, pg_db, test_db.version, pg_password
    ):
        connection_str = (f'postgresql+psycopg://{pg_user}:{pg_password}@'
                          f'{pg_host}:{pg_port}/{pg_db}')
        sessionmanager.init(connection_str)
        yield
        await sessionmanager.close()


@pytest.fixture(scope="function", autouse=True)
async def create_tables(connection_test):
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)


@pytest.fixture(scope="function", autouse=True)
async def session_override(app, connection_test):
    async def get_db_override():
        async with sessionmanager.session() as session:
            yield session
    app.dependency_overrides[get_async_session] = get_db_override


@pytest.fixture(scope="function", autouse=True)
async def test_session(connection_test):
    async with sessionmanager.session() as session:
        yield session


questions = [
    {
        'question_id': 123,
        'question': 'Test question0',
        'correct_answer': 'Test correct answer0',
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
        'add_date': datetime.now(),
    },
    {
        'question_id': 1134,
        'question': 'Test question1',
        'correct_answer': 'Test correct answer1',
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
        'add_date': datetime.now(),
    },
    {
        'question_id': 56723,
        'question': 'Test question2',
        'correct_answer': 'Test correct answer2',
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa2'),
        'add_date': datetime.now(),
    },
    {
        'question_id': 82791,
        'question': 'Test question3',
        'correct_answer': 'Test correct answer3',
        'answer': 'Test resceived answer',
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa3'),
        'add_date': datetime.now(),
    },
]


@pytest_asyncio.fixture(scope='function')
async def questions_in_db():
    async with sessionmanager.session() as session:
        created_questions = []
        for question_data in questions:
            question_schema = schemas.Question(**question_data)
            prepared_data = question_schema.dict()
            question = Question(**prepared_data)
            session.add(question)
            await session.commit()
            await session.refresh(question)
            created_questions.append(question.__dict__.copy())
        return created_questions


class MockResponse:
    def __init__(self, questions_num):
        self.status = 200
        self.questions_num = questions_num

    async def json(self):
        data = []
        for _ in range(self.questions_num):
            question_id = random.randint(1, 100000)
            data.append(
                {
                    'id': question_id,
                    'answer': f'Правильный ответ {question_id}',
                    'question': f'Вопрос {question_id}',
                }
            )
        return data

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self
