from django.shortcuts import render
from rest_framework.response import Response
from .Serializer import CreateAccountSerializer, LoginSerializer, MakeBillSerializer
from rest_framework.views import APIView
from django.utils.crypto import get_random_string
from .models import Profile, Bill
from rest_framework import status
# Create your views here.


def calculate_bill(previous, current):
    actual_valume = current - previous
    if actual_valume < 0:
        return 0
    elif actual_valume <= 5:
        return actual_valume * 340
    elif 5 < actual_valume <= 20:
        return actual_valume * 720
    elif 20 < actual_valume <= 50:
        return actual_valume * 845
    elif actual_valume > 50:
        return actual_valume * 877

    else:
        return "an error occurred"


def authenticate(token):
    try:
        account = Profile.objects.get(token=token)
        return account
    except Exception as e:
        return 0


class Login(APIView):
    def post(self, request):
        try:
            serialized_data = LoginSerializer(data=request.data)
            if serialized_data.is_valid():
                account = Profile.objects.get(
                    user_name=serialized_data.data.get('user_name'),
                    meter_number=serialized_data.data.get('password')
                )
                return Response(
                                {
                                    "user": {
                                        "username": account.user_name,
                                        "last_name": account.last_name,
                                        "meter_number": account.meter_number,
                                        "token": account.token,
                                    }
                                }
                                )
            else:
                return Response({"error": serialized_data.errors}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": str(e)})


class CreateAccount(APIView):
    def post(self, request):
        serialized_date = CreateAccountSerializer(data=request.data)
        if serialized_date.is_valid():
            account = Profile(
                                first_name=serialized_date.data.get('first_name'),
                                last_name=serialized_date.data.get('last_name'),
                                meter_number=serialized_date.data.get('meter_number'),
                                token=get_random_string(12, '0123456789'),
                                user_name=serialized_date.data.get('first_name')[0]+serialized_date.data.get('last_name')
                            )
            account.save()
            return Response(
                            {

                                "user": {
                                    "username": account.user_name,
                                    "last_name": account.last_name,
                                    "meter_number": account.meter_number,
                                    "token": account.token,
                                }
                            }
                            )
        else:
            return Response({"error": serialized_date.errors}, status=status.HTTP_401_UNAUTHORIZED)


class CalculateBillView(APIView):
    def post(self, request, token):
        try:
            answer = authenticate(token)
            if answer != 0:
                data_form = MakeBillSerializer(data=request.data)
                if data_form.is_valid():
                    bills = Bill.objects.filter(user=answer)
                    last_bill = bills.last()
                    # print(bills.last())
                    bill = Bill(user=answer, volume=data_form.data.get('volume'))
                    if last_bill == None:
                        if calculate_bill(0, data_form.data.get('volume'))==0:
                            return Response({"error": "the billing is not valid"}, status=status.HTTP_400_BAD_REQUEST)

                        bill.amount = calculate_bill(0, data_form.data.get('volume'))
                        bill.consumption = data_form.data.get('volume')
                    else:
                        if calculate_bill(last_bill.volume, data_form.data.get('volume'))==0:
                            return Response({"error": "the billing is not valid"}, status=status.HTTP_400_BAD_REQUEST)
                        bill.amount = calculate_bill(last_bill.volume, data_form.data.get('volume'))
                        bill.consumption = data_form.data.get('volume') - last_bill.volume
                    bill.save()
                    return Response({"message": True})
                else:
                    return Response({"errors": data_form.is_valid()}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": "Not authenticated as a user"}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DashboardView(APIView):
    def get(self, request, token):
        answer = authenticate(token)
        if answer != 0:
            bills = Bill.objects.filter(user=answer)
            serialized_bills = []
            for bill in bills:
                serialized_bills.append({
                    "date": bill.date,
                    "current_reading": bill.volume,
                    "previous_reading": bill.volume - bill.consumption,
                    "consumption": bill.consumption,
                    "cost": bill.amount,

                })
            return Response(serialized_bills)
        else:
            return Response({"error": "not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
