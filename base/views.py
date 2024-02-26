from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages # import the messages module
from django.http import JsonResponse
import openai

openai_api_key = "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" 
openai.api_key = openai_api_key
def ask_ai(message):
    response  = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {'role': 'system', 'content': "assistent"},
            {'role': 'user',   'content': message},
        ],
    )
    answer = response.choices[0].message.content.strip()
    return answer

def chatbot(request):
    if request.method == "POST":
        messege = request.POST.get('message')
        response =ask_ai(messege)
        context = {
            'message':messege,
            'response':response
            
        }
        return JsonResponse(context)
    return render(request,'base/chatbot.html')

def log_in(request):
    if request.user.is_authenticated:
        return redirect('chatbot')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User does not exist") # display flash message
        users = authenticate(username=username, password=password)
        if users is not None:
            login(request, user)
            return redirect('chatbot')
    return  render(request, 'login.html')

def log_out(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, "Passwords do not match") # display flash message
        else:
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                )
                user.save()
                return  redirect('chatbot')
            except:
                messages.error(request, "Username or Email already exists") # display flash message
    return render(request, 'base/register.html')