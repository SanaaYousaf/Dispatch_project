from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, MultiPartParser
from .serializer import *
from rest_framework.response import Response
from .models import User, Order
from .utils import send_otp_via_email
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from dispatch.permissions import IsOwnerOrReadOnly


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_otp_via_email(serializer.data['email'])
        user_data = serializer.data

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyView(generics.GenericAPIView):
    serializer_class = VerifyAccountSerializer

    def post(self, request):
        serializer = VerifyAccountSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            otp = serializer.data['otp']

            user = User.objects.filter(email=email)
            if not user.exists():
                return Response('invalid email', status=status.HTTP_400_BAD_REQUEST)
            if user[0].otp != otp:
                return Response('wrong otp', status=status.HTTP_400_BAD_REQUEST)
            user = user.first()
            user.is_active = True
            user.save()
            return Response('account verified', status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DispatchView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DispatchSerializer
    parser_classes = [MultiPartParser]

    def get(self, request):
        snippets = Dispatch.objects.filter(order__user=str(request.user.id))
        serializer = DispatchSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = DispatchSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.validated_data.get('order')
            if order.user.id == request.user.id:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(data='enter a valid order', status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrderSerializer

    def get(self, request):
        snippets = Order.objects.filter(user=str(request.user.id))
        serializer = OrderSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            if user.id == request.user.id:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(data='enter a valid user', status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DispatchDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Dispatch.objects.all()
    serializer_class = DispatchSerializer

