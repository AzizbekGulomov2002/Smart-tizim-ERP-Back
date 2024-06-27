from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import User, Company, Position
from .serializers import CompanySerializer, UserSerializer, PositionSerializer
from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.authtoken.models import Token
from .decorator import is_user_permission
class CreateCompanyUserAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        company_serializer = CompanySerializer(data=request.data.get('company'))
        user_serializer = UserSerializer(data=request.data.get('user'))

        if user_serializer.is_valid():
            if company_serializer.is_valid():
                company_instance = company_serializer.save()
                user_instance = user_serializer.save(
                    company_id=company_instance.id,
                    is_user_create=True,
                    is_trade=True,
                    is_client=True,
                    is_product=True,
                    is_finance=True,
                    is_statistics=True,
                    is_storage=True,
                )
                hashed_password = str(make_password(user_instance.password))
                user_instance.password = hashed_password
                user_instance.save()
                return Response({"user": user_serializer.data, "company": company_serializer.data},
                                status=status.HTTP_201_CREATED)

            return Response({"error": "Kompaniya nomi yoki telefon raqami unikal bo'lishi kerak"},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Barcha ma'lumotlarni to'ldirish zarur"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        companies = Company.objects.all()
        users = User.objects.all()
        company_serializer = CompanySerializer(companies, many=True)
        user_serializer = UserSerializer(users, many=True)
        return Response({"companies": company_serializer.data, "users": user_serializer.data},
                        status=status.HTTP_200_OK)



class PositionViewSet(ModelViewSet):
    permission_classes= [IsAuthenticated]
    serializer_class = PositionSerializer
    def get_queryset(self):
        company_id = self.request.user.company_id
        queryset = Position.objects.filter(company_id=company_id)
        return queryset
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company_id=request.user.company_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class UserCreateAPIView(APIView):
    permission_classes =[IsAuthenticated]

    @is_user_permission
    def post(self, request):
        password = request.data.pop('password', None)
        if password:
            request.data['company_id'] = request.user.company_id
            request.data['password'] = make_password(password)

        company = Company.objects.get(id=request.user.company_id)
        user_count = User.objects.filter(company_id=request.user.company_id).count()

        if (company.tariff == "BASIC" and user_count < 2) or \
                (company.tariff == "STANDART" and user_count < 100) or \
                (company.tariff == "BEST"):
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"error": "Bu foydalanuvchi allaqachon mavjud"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Tarif rejangizdagi foydalanuvchilar son limiti tugadi"}, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            # noqa multilanguage
            return Response({"error": {"message": "Foydalanuvchi nomi va parol kiritilishi kerak"}}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": {"message": "Foydalanuvchi topilmadi"}}, status=status.HTTP_404_NOT_FOUND)
        if not check_password(password, user.password):
            return Response({"error": {"message": "Parolda xatolik"}}, status=status.HTTP_401_UNAUTHORIZED)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class MeView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    def get(self, request):
        user = request.user
        if user.is_anonymous:
            return Response({
                "error": {
                    "message": "Bunday foydalanuvchi mavjud emas.",
                    "code": "unauthorized"
                }
            }, status=status.HTTP_401_UNAUTHORIZED)
        try:
            company = Company.objects.get(id=user.company_id)  # Assuming user.company_id is valid
            user_serializer = UserSerializer(user)
            company_serializer = CompanySerializer(company)
            return Response({
                "user": user_serializer.data,
                "company": company_serializer.data
            }, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({
                "error": {
                    "message": "Korxonada bunday foydalanuvchi mavjud emas",
                    "code": "not_found"
                }
            }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        user = request.user
        data = request.data

        # Update user information
        user.username = data.get('username', user.username)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        # Check if password is provided and hash it
        password = data.get('password')
        if password:
            user.password = make_password(password)

        # Save user instance
        user.save()

        # Return updated user data
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)







