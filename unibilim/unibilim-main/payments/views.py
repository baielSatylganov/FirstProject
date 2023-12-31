from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Payments
from .serializers import PaymentsSerializer, InitiatePaymentSerializer, ResponseSerializer
from django.shortcuts import get_object_or_404
from django.http import Http404
from random import shuffle
import requests
import hashlib
from drf_yasg.utils import swagger_auto_schema
from students.models import Student
from professors.models import Professors
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import logging
from .models import Payments
from meetings.models import Meetings
import datetime

@method_decorator(csrf_exempt, name='dispatch')
class PaymentResultView(View):
    def post(self, request, *args, **kwargs):
        # Получите данные из POST-запроса
        payment_id = request.POST.get('payment_id')
        status = request.POST.get('status')  # Примерно так, но структура может отличаться
        logger = logging.getLogger(__name__)

        # ... в вашем представлении ...
        body = request.body.decode('utf-8')
        logger.info(f"Received payment notification: {body}")
        # Найдите соответствующий платеж в вашей базе данных
        try:
            payment = Payments.objects.get(id=payment_id)
        except Payments.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Payment not found'}, status=404)
        
        # Обновите статус платежа
        logger.info(f"Current payment status: {payment.status}")
        if status == 'success':
            payment.status = 'COMPLETED'
            for slot in payment.time_slots:
                meeting_time = datetime.datetime.strptime(slot, "%Y-%m-%dT%H:%M:%S")  
                Meetings.objects.create(
                    subject=payment.service,
                    student=payment.student,
                    professor=payment.professor,
                    datetime=meeting_time,
                    status='PENDING'
        )       
        else:
            payment.status = 'DECLINED'
        logger.info(f"Updated payment status: {payment.status}")        
        payment.save()
        
        return JsonResponse({'status': 'success', 'message': 'Payment status updated successfully'})


class InitiatePaymentView(APIView):
    @swagger_auto_schema(
    request_body=InitiatePaymentSerializer,
    responses={200: ResponseSerializer()},
    operation_description="""
    Endpoint инициирует процесс оплаты и возвращает ответ в формате XML. 
    Поле 'time_slots' ожидает список объектов.
    Каждый объект должен быть строкой, содержащей дату и время в формате 'YYYY-MM-DDTHH:MM:SS'. 
    Например: '2023-07-20T14:30:00'.
    """
)

    def post(self, request, format=None):
        student_id = request.user.student.id
        student = Student.objects.get(id=student_id)
        professor_id = request.data.get('professor_id') 
        professor = Professors.objects.get(id=professor_id)
        time_slots = request.data.get('time_slots') 
        amount_per_slot = request.data.get('amount') 
        service = request.data.get('service') 

        total_amount = len(time_slots) * amount_per_slot

        

        # формирование описания платежа
        description_lines = []
        for slot in time_slots:  
            description_lines.append(f'Payment for {service}({slot})')

        description = '\n'.join(description_lines)
        
        

        # создаем запись платежа в базе данных
        payment = Payments.objects.create(
            amount=total_amount,
            student=student,
            description=description,
            service=service,
            status='PENDING',
            professor=professor,
            time_slots=time_slots,
        )

        payment_data = self.initiate_payment(total_amount, description, student_id, payment.id)
        # возвращаем ответ с информацией о платеже
        serializer = PaymentsSerializer(payment)
        
        return Response({         
            'payment_data': payment_data
        })

    def initiate_payment(self, amount, description, user_id, payment_id ):
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

        pg_salt = list('qwertyuiolkjhgfdsazxcvbnm')
        shuffle(pg_salt)
        pg_salt = ''.join(pg_salt)

        pg_merchant_id = 530056  # замените на ваш идентификатор мерчанта
        secret_key = 'BDHwOaU4Kbl1UE3M'  # замените на ваш секретный ключ

        request = {
            'pg_order_id': str(payment_id),  # преобразовываем user_id в строку, так как все значения должны быть строками
            'pg_merchant_id': pg_merchant_id,
            'pg_amount': str(amount),
            'pg_description': description,  # используем описание, которое мы сформировали ранее
            'pg_salt': pg_salt,
            'pg_success_url': 'http://13.53.177.204/professors/',
            'pg_failure_url': 'http://13.53.177.204/students/',
            'pg_currency': 'KGS',
            'pg_request_method': 'POST',            
            'pg_language': 'ru',
            'pg_result_url': 'http://13.53.177.204/check_payment/',
            'pg_testing_mode': '1',
            'pg_user_id': str(user_id),     
        }

        request_for_signature = make_flat_params_array(request)
        request_for_signature.insert(0, ("method_name", "init_payment.php"))
        request_for_signature.append(("secret_key", secret_key))

        pg_sig = hashlib.md5(';'.join(x[1] for x in request_for_signature).encode()).hexdigest()   
        request['pg_sig'] = pg_sig    

        # Вы можете реализовать проверку ответа здесь, если это необходимо
        response = requests.post('https://api.freedompay.money/init_payment.php', data=request)

        return response  # Вы можете вернуть более полезные данные здесь, например response.json(), если это необходимо


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

'''
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
   
    
    pg_merchant_id = 530056  # замените на ваш идентификатор мерчанта
    secret_key = 'BDHwOaU4Kbl1UE3M'  # замените на ваш секретный ключ
   # pg_order_id = 

    request = {
        'pg_order_id': '23',
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

    pg_sig = hashlib.md5(';'.join(x[1] for x in request_for_signature).encode()).hexdigest()   
    request['pg_sig'] = pg_sig    
    return request

request = create_request()
response = requests.post('https://api.freedompay.money/get_status.php', data=request)

request = create_request()
response = requests.post('https://api.freedompay.money/init_payment.php', data=request)

'''