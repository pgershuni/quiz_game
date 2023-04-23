import requests

response = requests.post('http://127.0.0.1:8080/api/users', json={'name': 'пользователь1',
                                                                  'about': 'о пользователе',
                                                                  'login': 'логин1',
                                                                  'password': 'пароль1'})
print(response.json())

response = requests.post('http://127.0.0.1:8080/api/users', json={'name': 'имя пользователя',
                                                                  'about': 'о пользователе',
                                                                  'login': 'логин',
                                                                  'password': 'пароль'})

print(response.json())
response = requests.post('http://127.0.0.1:8080/api/telegram_keys', json={'user_id': 2})
print(response.json())

response = requests.post('http://127.0.0.1:8080/api/telegram_keys', json={'user_id': 1})
print(response.json())

response = requests.post('http://127.0.0.1:8080/api/tests', json={'title': 'Тест', 'category': 'Химия',
                                                                  'about': 'о чем тест',
                                                                  'questions': [
                                                                      {'type': 'ord',
                                                                       'question': 'вопрос',
                                                                       'answer': 'ответ'},
                                                                      {'type': 'rad',
                                                                       'question': ['сам вопрос',
                                                                                    ['вариант1', 'правильный вариант',
                                                                                     'варианты2']],
                                                                       'answer': 'правильный вариант'},
                                                                      {'type': 'check',
                                                                       'question': ['сам вопрос',
                                                                                    ['вариант1 правильный', 'вариант2',
                                                                                     'вариант3 правильный',
                                                                                     'вариант3', 'вариант4']],
                                                                       'answer': ['вариант1 правильный',
                                                                                  'вариант3 правильный']}],
                                                                  'is_private': False,
                                                                  'user_id': 1})
print(response.json())
