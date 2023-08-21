import requests
import json

# URL вашего API-представления
url = 'http://13.53.177.204//init_payment/'

# Здесь укажите свои данные
data = {
    'professor_id': '1',
    'time_slots': ['2023-07-20T14:30:00', '2023-07-21T15:00:00'],
    'amount': 3,
    'service': 'ServiceName'
}

headers = {
    'Authorization': 'Token b13df40f968f018b00424fad00fffd51cd406c20',  # Если ваше API требует аутентификацию, замените YOUR_ACCESS_TOKEN на ваш токен
    'Content-Type': 'application/json'
}
response = requests.post(url, data=json.dumps(data), headers=headers)

print(response.status_code)
print(response.json())


# # import requests
# # import json

# # # URL вашего API-представления
# # url = 'http://13.53.177.204/professors/'

# # # Здесь укажите свои данные
# # data = {
# #     'professor_id': '1',
# #     'time_slots': ['2023-07-20T14:30:00', '2023-07-21T15:00:00'],
# #     'amount': 100,
# #     'service': 'ServiceName'
# # }

# # headers = {
# #     'Authorization': 'Token 2d00fd8975336f24addbf078130908cb8396690b',  # Если ваше API требует аутентификацию, замените YOUR_ACCESS_TOKEN на ваш токен
# #     'Content-Type': 'application/json'}
# # response = requests.get(url,  headers=headers)
# # print(response.json())



# import requests

# api_url = "http://13.53.177.204/"  # Замените на фактический URL вашего API
# token = "bae061df17a4a3fec4437e4243554f6cd7925ef2"  # Замените на ваш полученный токен

# headers = {
#     "Authorization": f"Token {token}"
# }

# # Выполнение GET-запроса к защищенному ресурсу
# response = requests.get(f"{api_url}/professors/my_students/", headers=headers)

# if response.status_code == 200:
#     professors_list = response.json()
#     print("Список профессоров:", professors_list)
# elif response.status_code == 401:
#     print("Недостаточно аутентификационных данных.")
# else:
#     print("Ошибка:", response.status_code)


    