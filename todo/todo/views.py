from django.shortcuts import get_object_or_404, redirect, render # type: ignore
from django.contrib.auth.models import User # type: ignore
from todo import models
from todo.models import TODOO
from . import models
from django.contrib.auth import authenticate, login as auth_login, logout # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.shortcuts import render, redirect # type: ignore
from django.contrib import messages # type: ignore

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('frm')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'signup.html')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'signup.html')
        
        # Validate input
        if not username or not email or not password:
            messages.error(request, 'Please fill all fields')
            return render(request, 'signup.html')
        
        try:
            # Create user
            my_user = User.objects.create_user(username, email, password)
            my_user.save()
            messages.success(request, 'Account created successfully')
            return redirect('/login')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'signup.html')
    
    return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        frm = request.POST.get('frm')
        pwd = request.POST.get('pwd')
        print(frm, pwd)
        userr = authenticate(request, username=frm, password=pwd)
        if userr is not None:
            # Use auth_login instead of login
            auth_login(request, userr)
            return redirect('/todopage')
        else:
            return redirect('/login')
        
    return render(request, 'login.html')

@login_required(login_url='/login') # type: ignore

def todo(request):
    if request.method=='POST':
        title = request.POST.get('title')
        print(title)
        obj = models.TODOO(title = title, user = request.user)
        obj.save()
        user = request.user
        res = models.TODOO.objects.filter(user = request.user).order_by('-date')
        return redirect('/todopage', {'res':res})
    res = models.TODOO.objects.filter(user = request.user).order_by('-date')
    return render(request, 'todo.html', {'res':res})

@login_required(login_url='/login') # type: ignore

def edit_todo(request, srno):
    obj = get_object_or_404(models.TODOO, srno=srno) # type: ignore
    
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:  # Optional: validate that title is not empty
            obj.title = title
            obj.save()
        return redirect('/todopage')
    
    return render(request, 'edit_todo.html', {'obj': obj})

@login_required(login_url='/login') # type: ignore

def delete_todo(request, srno):
    obj = get_object_or_404(models.TODOO, srno=srno, user=request.user)
    obj.delete()
    return redirect('/todopage')

def signout(request):
    logout(request)
    return redirect('/login')

