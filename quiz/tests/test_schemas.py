from datetime import datetime
from uuid import UUID

import pytest

from business_layer import schemas

valid_question_data = [
    {
        'question_id': 123,
        'question': 'T' * 255,
        'correct_answer': 'r' * 255,
        'answer': 'd' * 255,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
        'add_date': datetime.now(),
    },
    {
        'question_id': 1,
        'question': '',
        'correct_answer': '',
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
        'add_date': datetime.now(),
    },
]
invalid_question_data = [
    {
        'question_id': 0,
        'question': 'T' * 255,
        'correct_answer': 'r' * 255,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
        'add_date': datetime.now(),
    },
    {
        'question_id': 1,
        'question': 'T' * 256,
        'correct_answer': 'r' * 255,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
        'add_date': datetime.now(),
    },
    {
        'question_id': 1,
        'question': 'T' * 255,
        'correct_answer': 'r' * 256,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
        'add_date': datetime.now(),
    },
    {
        'question_id': 1,
        'question': 'T' * 255,
        'correct_answer': 'r' * 256,
        'quiz_id': 'ddd',
        'add_date': datetime.now(),
    },
    {
        'question_id': 1,
        'question': 'T' * 255,
        'correct_answer': 'r' * 255,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
        'add_date': 'ddd',
    },
    {
        'question_id': 123,
        'question': 'T' * 255,
        'correct_answer': 'r' * 255,
        'answer': 'd' * 256,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
        'add_date': datetime.now(),
    },
    {
        'question': 'T' * 255,
        'correct_answer': 'r' * 255,
        'answer': 'd' * 255,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
        'add_date': datetime.now(),
    },
    {
        'question_id': 123,
        'correct_answer': 'r' * 255,
        'answer': 'd' * 255,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
        'add_date': datetime.now(),
    },
    {
        'question_id': 123,
        'question': 'T' * 255,
        'answer': 'd' * 255,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
        'add_date': datetime.now(),
    },
    {
        'question_id': 123,
        'question': 'T' * 255,
        'correct_answer': 'r' * 255,
        'answer': 'd' * 255,
        'add_date': datetime.now(),
    },
    {
        'question_id': 123,
        'question': 'T' * 255,
        'correct_answer': 'r' * 255,
        'answer': 'd' * 255,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
    },
    {},
]
valid_answer_data = [
    {
        'question_id': 123,
        'answer': 'd' * 255,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
    },
    {
        'question_id': 1,
        'answer': '',
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
    },
]
invalid_answer_data = [
    {
        'question_id': 0,
        'answer': 'd' * 255,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
    },
    {
        'question_id': 123,
        'answer': 'd' * 256,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
    },
    {
        'question_id': 123,
        'answer': 'd' * 255,
        'quiz_id': 'ffff',
    },
    {

        'answer': 'd' * 255,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
    },
    {
        'question_id': 123,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
    },
    {
        'question_id': 123,
        'answer': 'd' * 255,
    },
]
valid_quiz_full_data = [
    {
        'question_id': 123,
        'question': 'd' * 255,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
        'previous_question_correct_answer': 'd' * 255,
    },
    {
        'question_id': 1,
        'question': '',
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
        'previous_question_correct_answer': '',
    },
    {
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
    },
]
invalid_quiz_full_data = [
    {
        'question_id': 0,
        'question': 'd' * 255,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
        'previous_question_correct_answer': 'd' * 255,
    },
    {
        'question_id': 123,
        'question': 'd' * 256,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
        'previous_question_correct_answer': 'd' * 255,
    },
    {
        'question_id': 123,
        'question': 'd' * 255,
        'quiz_id': '',
        'previous_question_correct_answer': 'd' * 255,
    },
    {
        'question_id': 123,
        'question': 'd' * 255,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
        'previous_question_correct_answer': 'd' * 256,
    },
    {
        'question_id': 123,
        'question': 'd' * 255,
        'previous_question_correct_answer': 'd' * 255,
    },
]
valid_quiz_no_answer_data = [
    {
        'question_id': 123,
        'question': 'd' * 255,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
    },
    {
        'question_id': 1,
        'question': '',
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
    },
    {
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
    },
]
invalid_quiz_no_answer_data = [
    {
        'question_id': 0,
        'question': 'd' * 255,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
    },
    {
        'question_id': 123,
        'question': 'd' * 256,
        'quiz_id': UUID('a038f779-2c66-4565-90e8-8507da656fa1'),
    },
    {
        'question_id': 123,
        'question': 'd' * 255,
        'quiz_id': 111,
    },
    {
        'question_id': 123,
        'question': 'd' * 255,
    },
]
valid_initiate_quiz_data = [
    {
        'questions_num': 1,
    },
    {
        'questions_num': 100,
    },
]
invalid_initiate_quiz_data = [
    {
        'questions_num': 0,
    },
    {
        'questions_num': 101,
    },
    {
        'questions_num': 'ddd',
    },
]

valid_data_schema = [
    (valid_answer_data, schemas.QuizAnswer),
    (valid_initiate_quiz_data, schemas.InitiateQuiz),
    (valid_question_data, schemas.Question),
    (valid_quiz_full_data, schemas.QuizResponseFull),
    (valid_quiz_no_answer_data, schemas.QuizResponseNoAnswer),
]

invalid_data_schema = [
    (invalid_answer_data, schemas.QuizAnswer),
    (invalid_initiate_quiz_data, schemas.InitiateQuiz),
    (invalid_question_data, schemas.Question),
    (invalid_quiz_full_data, schemas.QuizResponseFull),
    (invalid_quiz_no_answer_data, schemas.QuizResponseNoAnswer),
]


@pytest.mark.parametrize('data_list, schema', valid_data_schema)
def test_schema_object_is_created_with_valid_data(data_list, schema):
    for input_data in data_list:
        output = schema(**input_data)
        output_data = output.model_dump()
        field_names = list(input_data.keys())
        for name in field_names:
            assert output_data[name] == input_data[name], (
                f'{schema.__name__}, {input_data}')


@pytest.mark.parametrize('data_list, schema', invalid_data_schema)
def test_schema_object_is_not_created_with_invalid_data(data_list, schema):
    for input_data in data_list:
        with pytest.raises(Exception):
            schema(**input_data)
