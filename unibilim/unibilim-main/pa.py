import requests

# URL вашего эндпоинта
url = 'http://13.53.177.204/check_payment/'

# Данные, которые вы хотите отправить
data = {
    'payment_id': '11',  # Убедитесь, что у вас есть платеж с этим ID в базе данных
    'status': 'success'
}

# Отправка POST-запроса
response = requests.post(url, data=data)

# Вывод ответа
print(response.status_code)