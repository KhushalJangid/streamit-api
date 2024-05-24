from json import dumps, loads
from rest_framework import exceptions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import (SAFE_METHODS, AllowAny, BasePermission,
                                        IsAuthenticated)
from rest_framework.response import Response
from rest_framework.views import APIView
from account.models import Key, User
from account.verify import get_otp, send_otp



def parseGet(request,kw):
    _ = request.query_params.get(kw)
    if _:
        return _
    else:
        return ""


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class WriteOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['POST']


class UserView(APIView):
    # * allow post requests but authenticate get/update requests
    permission_classes = [IsAuthenticated | WriteOnly]
    authentication_classes = [TokenAuthentication, ]

    def get(self, format=None):
        '''This function returns the data of requested user'''
        id = self.request.query_params.get("id")
        try:
            user = User.objects.get(id=id)
            data = user.toJson()
            return Response(data)
        except:
            raise exceptions.AuthenticationFailed("Inavlid User Id")

    def post(self, request):
        data = request.data
        email = data.get("email")
        if email :
            '''This part of function is used to SignUp a user via Email.'''
            if "name" in data and "password" in data:
                name = data["name"]
                f_name = name.split()[0]
                l_name = name.split()[-1]
                password = data["password"]
                try:
                    user = User.objects.create(first_name=f_name,
                                                last_name=l_name,
                                                email=email,
                                                is_active=False)
                    user.set_password(password)
                except:
                    return Response({"error": "User with the email already exists.Login instead."}, status=status.HTTP_400_BAD_REQUEST)
                OTP, token = OtpVerify.create(user)
                send_otp(email=email, otp=OTP, name=name)
                data = {
                    "token": token,
                    "id": user.id
                }
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Incomplete Data"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': "Email is required"}, status=status.HTTP_400_BAD_REQUEST)



@permission_classes([AllowAny])
@api_view(['POST'])
def Login(request):
    '''This function is used to login a user via Email and
     return the Token for further transactions'''

    from django.contrib.auth import authenticate
    try:
        map = loads(request.body)
        password = map["password"]
        try:
            user = User.objects.get(email=map["email"])
            user = authenticate(username=user.username, password=password)
            # print(type(user))
            if user is None:
                return Response({"error":"Incorrect Password."},status=status.HTTP_400_BAD_REQUEST)
            token, created = Token.objects.get_or_create(user=user)
            # print(token)
            data = {
                "token": token.key,
                "id": user.id
            }
            return Response(data,status= status.HTTP_202_ACCEPTED)
        except Exception as e:
            print(e)
            return Response({"error":"Email not registered."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OtpVerify(APIView):
    authentication_classes(IsAuthenticated)

    def create(user):
        token, created = Token.objects.get_or_create(user=user)
        OTP = get_otp()
        try: 
            Key.objects.create(id=user.id, otp=OTP, key=str(token.key), expiry=600)
        except :
            obj = Key.objects.get(id=user.id)
            obj.otp = OTP
            obj.key = token.key
            obj.save()
        return OTP, token.key

    def post(self, request):
        try:
            data = request.data
            otp = data["otp"]
            token = data["token"]
            try:
                key = Key.objects.get(key=token)
            except Key.DoesNotExist:
                return Response({"error": "Token does not match."}, status=status.HTTP_400_BAD_REQUEST)
            if otp == key.otp:
                uid = Token.objects.get(key=token).user.id
                user = User.objects.get(id=uid)
                user.is_active = True
                user.save()
                data = user.toJson()
                return Response(data, status=status.HTTP_202_ACCEPTED)
            else:
                return Response({"error": "Otp does not match."}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({"error":"OTP is required."},status=status.HTTP_400_BAD_REQUEST)

    
    
    