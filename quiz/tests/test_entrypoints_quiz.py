from db_layer.crud import question_crud
from tests.conftest import MockResponse, questions


def test_quiz_get_question_returns_correct_data(client, questions_in_db):
    """Эндпойнт для получения следующего вопроса возвращает корректные
    данные."""
    expected_question = questions[2]
    expected_quiz_id = str(expected_question['quiz_id'])
    expected_keys = sorted(['question_id', 'question', 'quiz_id'])
    response = client.get(f'/api/v1/quiz/next_question/{expected_quiz_id}')
    assert response.status_code == 200, 'Неверный код ответа'
    data = response.json()
    response_keys = sorted(list(data.keys()))
    assert response_keys == expected_keys
    assert data['question_id'] == expected_question['question_id']
    assert data['question'] == expected_question['question']
    assert data['quiz_id'] == expected_quiz_id


def test_quiz_get_question_on_finished_quiz_returns_404(
    client,
    questions_in_db,
):
    """Эндпойнт для получения следующего вопроса не возвращает вопрос,
    если на все вопросы уже получены ответы."""
    expected_question = questions[3]
    expected_quiz_id = str(expected_question['quiz_id'])
    response = client.get(f'/api/v1/quiz/next_question/{expected_quiz_id}')
    assert response.status_code == 404, 'Неверный код ответа'


def test_quiz_get_question_uknown_quiz_id_returns_404(client, questions_in_db):
    """Эндпойнт для получения следующего вопроса не возвращает вопрос,
    если номер викторины не найден."""
    quiz_id = 'a038f779-2c66-4565-90e8-8507da656fa3'
    response = client.get(f'/api/v1/quiz/next_question/{quiz_id}')
    assert response.status_code == 404, 'Неверный код ответа'


def test_quiz_get_question_invalid_quiz_id_returns_422(
    client,
    questions_in_db
):
    """Эндпойнт для получения следующего вопроса возвращает статус-код 422,
    если в путь передан не UUID."""
    quiz_id = 'ab;skdlksldfkjnv'
    response = client.get(f'/api/v1/quiz/next_question/{quiz_id}')
    assert response.status_code == 422, 'Неверный код ответа'
    data = response.json()
    assert list(data.keys()) == ['detail']


async def test_quiz_answer_post_saves_answer_and_returns_correct_data(
    client,
    questions_in_db,
    test_session,
):
    """Эндпойнт для отправки ответа на вопрос сохраняет ответ в БД,
    после чего возвращает правильный ответ и следующий вопрос."""
    input_data = {
        'quiz_id': str(questions[0]['quiz_id']),
        'question_id': questions[0]['question_id'],
        'answer': 'Input answer',
    }
    expected_question_id = questions[1]['question_id']
    expected_question_text = questions[1]['question']
    expected_quiz_id = str(questions[1]['quiz_id'])
    expected_answer = questions[0]['correct_answer']
    expected_keys = sorted(['question_id', 'question', 'quiz_id',
                            'previous_question_correct_answer'])

    response = client.post('/api/v1/quiz/answer', json=input_data)
    assert response.status_code == 200, 'Неверный код ответа'

    data = response.json()
    response_keys = sorted(list(data.keys()))
    assert response_keys == expected_keys
    assert data['question'] == expected_question_text
    assert data['question_id'] == expected_question_id
    assert data['previous_question_correct_answer'] == expected_answer
    assert data['quiz_id'] == expected_quiz_id

    saved_question = await question_crud.get(
        questions[0]['question_id'],
        test_session
    )
    assert saved_question.answer == input_data['answer']


async def test_quiz_answer_post_last_question_returns_no_question(
    client,
    questions_in_db,
    test_session,
):
    """При отправке на эндпойнт ответов ответа на последний вопрос
    викторины с данным id возвращается только правильный ответ."""
    input_data = {
        'quiz_id': str(questions[2]['quiz_id']),
        'question_id': questions[2]['question_id'],
        'answer': 'Input answer',
    }
    expected_quiz_id = str(questions[2]['quiz_id'])
    expected_answer = questions[2]['correct_answer']
    expected_keys = sorted(['quiz_id', 'previous_question_correct_answer'])

    response = client.post('/api/v1/quiz/answer', json=input_data)
    assert response.status_code == 200, 'Неверный код ответа'

    data = response.json()
    response_keys = sorted(list(data.keys()))
    assert response_keys == expected_keys
    assert data['previous_question_correct_answer'] == expected_answer
    assert data['quiz_id'] == expected_quiz_id

    saved_question = await question_crud.get(
        questions[2]['question_id'],
        test_session
    )
    assert saved_question.answer == input_data['answer']


async def test_quiz_answer_post_repeatable_answer_post_not_allowed(
    client,
    questions_in_db,
    test_session,
):
    """При отправке на эндпойнт ответов повторного ответа на вопрос
    возвращается статус 400, а в БД новый ответ не сохраняется."""
    input_data = {
        'quiz_id': str(questions[3]['quiz_id']),
        'question_id': questions[3]['question_id'],
        'answer': 'Amended input answer',
    }

    response = client.post('/api/v1/quiz/answer', json=input_data)
    data = response.json()
    assert response.status_code == 400, 'Неверный код ответа'
    assert list(data.keys()) == ['detail'], input_data

    saved_question = await question_crud.get(
        questions[3]['question_id'],
        test_session
    )
    assert saved_question.answer != input_data['answer']


async def test_quiz_answer_post_invalid_data_returns_422(
    client,
    questions_in_db,
):
    """При отправке на эндпойнт ответов невалидных
    данных возвращается статус 422."""
    invalid_data = [
        {
            'quiz_id': 'aaaa',
            'question_id': questions[0]['question_id'],
            'answer': 'Input answer',
        },
        {
            'quiz_id': str(questions[0]['quiz_id']),
            'question_id': 'sss',
            'answer': 'Input answer',
        },
        {
            'quiz_id': str(questions[0]['quiz_id']),
            'question_id': questions[0]['question_id'],
        },
    ]
    for input_data in invalid_data:
        response = client.post('/api/v1/quiz/answer', json=input_data)
        data = response.json()
        assert response.status_code == 422, input_data
        assert list(data.keys()) == ['detail'], input_data


async def test_quiz_answer_post_unexisted_data_returns_400(
    client,
    questions_in_db,
):
    """При отправке на эндпойнт ответов данных с несуществующим
    вопросом / несуществующим id викторины возвращается статус 400."""
    unexisted_data = [
        {
            'quiz_id': str(questions[0]['quiz_id']),
            'question_id': 999,
            'answer': 'Input answer',
        },
        {
            'quiz_id': 'a038f779-2c66-4565-90e8-8507da656fa0',
            'question_id': questions[0]['question_id'],
            'answer': 'Input answer',
        },
    ]
    for input_data in unexisted_data:
        response = client.post('/api/v1/quiz/answer', json=input_data)
        data = response.json()
        assert response.status_code == 400, input_data
        assert list(data.keys()) == ['detail'], input_data


async def test_quiz_post_invalid_data_returns_422(
    client,
    test_session,
):
    """При отправке на эндпойнт ответов невалидных
    данных возвращается статус 422."""
    invalid_data = [
        {
            'questions_num': 'abc',
        },
        {},
        {
            'num': 5,
        },
    ]
    for input_data in invalid_data:
        response = client.post('/api/v1/quiz', json=input_data)
        data = response.json()
        assert response.status_code == 422, input_data
        assert list(data.keys()) == ['detail'], input_data

        saved_questions = await question_crud.get_all(test_session)
        assert len(saved_questions) == 0


async def test_quiz_post_saves_questions_and_returns_correct_data(
    client,
    test_session,
    mocker,
):
    """При отправке на эндпойнт старта викторины корректного запроса
    вопросы в нужном кол-ве сохраняются в БД, после чего возвращается
    первый вопрос."""
    input_data = {'questions_num': 5}
    expected_keys = sorted(['question_id', 'question', 'quiz_id'])
    resp = MockResponse(input_data['questions_num'])
    mocker.patch('aiohttp.ClientSession.get', return_value=resp)
    response = client.post('/api/v1/quiz', json=input_data)
    data = response.json()
    assert response.status_code == 200
    assert sorted(list(data.keys())) == expected_keys
    saved_questions = await question_crud.get_all(test_session)
    assert len(saved_questions) == 5
