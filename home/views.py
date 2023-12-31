from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Profile
from .serializers import ProfileSerializer, UserSerializer, LoginSerializer, SignUpSerializer

# Create your views here.

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = user.profile

        serializer_user = UserSerializer(user)
        serializer_profile = ProfileSerializer(profile)

        return Response({
            'user': serializer_user.data,
            'profile': serializer_profile.data
        })

    def post(self, request, *args, **kwargs):
        profile_data = request.data
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=profile_data, partial=True)

        if serializer.is_valid():
            serializer.save(user=request.user)
            message = 'Profile created successfully' if created else 'Profile updated successfully'
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=400)

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            login(request, user)
            return Response(data)
        else:
            return Response({'error': 'Invalid credentials'}, status=401)

class SignUpView(APIView):
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()

        subject = 'Congrats!!!, Your account has been created'
        html_message = render_to_string('email.html', {
            'username': user.username,
        })

        plain_message = strip_tags(html_message)
        to_email = user.email
        msg = EmailMultiAlternatives(subject, plain_message, to=[to_email])
        msg.attach_alternative(html_message, "text/html")
        msg.send()

        data = {
            'message': 'User created successfully. Check your mail for username',
        }
        return Response(data)

@login_required
def index(request):
    return HttpResponse('User logged in: '+str(request.user))