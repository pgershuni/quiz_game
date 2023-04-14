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

response = requests.post('http://127.0.0.1:8080/api/tests', json={'title': 'название5',
              'about': 'о чем5',
              'questions': [
                {'type': 'ord',
                 'question':'Bопрос5',
                 'answer':'ответ52'},
                {'type': 'rad',
                 'question':['сам вопрос152', ['варианты выбора152', 'варианты выбора1251', 'варианты выбора2251']],
                 'answer':'ответ52'},
                {'type': 'check',
                 'question':['сам вопрос52', ['варианты выбора251', 'варианты выбора1251', 'варианты выбора2521']],
                 'answer':['ответы21', 'ответы121']}],
              'is_private': False,
              'user_id': 2})
print(response.json())

response = requests.post('http://127.0.0.1:8080/api/tests', json={'title': 'название',
              'about': 'о чем',
              'questions': [
                {'type': 'ord',
                 'question':'Bопрос',
                 'answer':'ответ2'},
                {'type': 'rad',
                 'question':['сам вопрос12', ['варианты выбора12', 'варианты выбора121', 'варианты выбора221']],
                 'answer':'ответ2'},
                {'type': 'check',
                 'question':['сам вопрос2', ['варианты выбора21', 'варианты выбора121', 'варианты выбора221']],
                 'answer':['ответы21', 'ответы121']}],
              'is_private': False,
              'user_id': 2})
print(response.json())

response = requests.post('http://127.0.0.1:8080/api/tests', json={'title': 'название теста1',
              'about': 'о чем тест1',
              'questions': [
                {'type': 'ord',
                 'question':'опрос1',
                 'answer':'ответ1'},
                {'type': 'rad',
                 'question':['сам вопрос1', ['варианты выбора1', 'варианты выбора11', 'варианты выбора21']],
                 'answer':'ответ'},
                {'type': 'check',
                 'question':['сам вопрос', ['варианты выбора1', 'варианты выбора11', 'варианты выбора21']],
                 'answer':['ответы1', 'ответы11']}],
              'is_private': False,
              'user_id': 2})
print(response.json())


response = requests.post('http://127.0.0.1:8080/api/tests', json={'title': 'название теста',
              'about': 'о чем тест',
              'questions': [
                {'type': 'ord',
                 'question':'опрос',
                 'answer':'ответ'},
                {'type': 'rad',
                 'question':['сам вопрос', ['варианты выбора', 'варианты выбора1', 'варианты выбора2']],
                 'answer':'ответ'},
                {'type': 'check',
                 'question':['сам вопрос', ['варианты выбора', 'варианты выбора1', 'варианты выбора2']],
                 'answer':['ответы', 'ответы1']}],
              'is_private': False,
              'user_id': 1})
print(response.json())
