import hashlib
import requests
from random import shuffle


# def initiate_payment(amount, description, user_id):
#         def make_flat_params_array(arr_params, parent_name=''):
#             arr_flat_params = []
#             i = 0
#             for key in sorted(arr_params.keys()):
#                 i += 1
#                 val = arr_params[key]
#                 name = f'{parent_name}{key}{str(i).zfill(3)}'
#                 if isinstance(val, dict):
#                     arr_flat_params.extend(make_flat_params_array(val, name))
#                     continue
#                 arr_flat_params.append((name, str(val)))
#             return arr_flat_params

#         pg_salt = list('qwertyuiolkjhgfdsazxcvbnm')
#         shuffle(pg_salt)
#         pg_salt = ''.join(pg_salt)

#         pg_merchant_id = 530056  # замените на ваш идентификатор мерчанта
#         secret_key = 'BDHwOaU4Kbl1UE3M'  # замените на ваш секретный ключ

#         request = {
#             'pg_order_id': str(user_id),  # преобразовываем user_id в строку, так как все значения должны быть строками
#             'pg_merchant_id': pg_merchant_id,
#             'pg_amount': amount,
#             'pg_description': description,  # используем описание, которое мы сформировали ранее
#             'pg_salt': pg_salt,
#             'pg_currency': 'KGS',
#             'pg_request_method': 'POST',
#             'pg_language': 'ru',
#             'pg_testing_mode': '1',
#             'pg_user_id': '435',     
#         }

#         request_for_signature = make_flat_params_array(request)
#         request_for_signature.insert(0, ("method_name", "get_status.php"))
#         request_for_signature.append(("secret_key", secret_key))

#         pg_sig = hashlib.md5(';'.join(x[1] for x in request_for_signature).encode()).hexdigest()   
#         request['pg_sig'] = pg_sig    

#         # Вы можете реализовать проверку ответа здесь, если это необходимо
#         response = requests.post('https://api.freedompay.money/init_payment.php', data=request)

#         return response.text
    
# print(initiate_payment(20, 'test', '3'))




def make_flat_params_array(arr_params, parent_name=''):
        arr_flat_params = []
        i = 0
        for key in sorted(arr_params.keys()):
            i += 1
            val = arr_params[key]
            name = f'{parent_name}{key}{str(i).zfill(3)}'
            if isinstance(val, dict):
                arr_flat_params.extend(make_flat_params_array(val, name))
                continue
            arr_flat_params.append((name, str(val)))
        return arr_flat_params
    
    
def create_request():
    pg_salt = list('qwertyuiolkjhgfdsazxcvbnm')
    shuffle(pg_salt)
    pg_salt = ''.join(pg_salt)
   
    
    pg_merchant_id = "530056"  # замените на ваш идентификатор мерчанта
    secret_key = 'BDHwOaU4Kbl1UE3M'  # замените на ваш секретный ключ
   # secret_key = 'F843jLrE6xX3HEYD'
   # pg_order_id = 

    request = {
        'pg_order_id': '6',
        'pg_merchant_id': pg_merchant_id,
        'pg_amount': '25',
        'pg_description': 'test',
        'pg_salt': pg_salt,
        'pg_currency': 'KGS',
        'pg_request_method': 'POST',
        'pg_language': 'ru',
        'pg_testing_mode': '1',
        'pg_user_id': '1',     
    }

    

    request_for_signature = make_flat_params_array(request)
    request_for_signature.insert(0, ("method_name", "get_status.php"))
    request_for_signature.append(("secret_key", secret_key))
    print(';'.join(x[1] for x in request_for_signature))
    pg_sig = hashlib.md5(';'.join(x[1] for x in request_for_signature).encode()).hexdigest()   
    request['pg_sig'] = pg_sig    
    return request

request = create_request()
response = requests.post('https://api.freedompay.money/get_status.php', data=request)
print(response.text)
# request = create_request()
# response = requests.post('https://api.freedompay.money/init_payment.php', data=request)
# print(response.text)