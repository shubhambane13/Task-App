from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from Task_app.forms import TaskAppForm
from Task_app.models import TaskApp
from random import randrange
from django.core.mail import send_mail
from todoapp.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


def home(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'index.html')
    else:
        return redirect('ulogin')

# authentication part(closed)
def usignup(request):
	if request.method=="POST":
		em=request.POST.get("em")
		try:
			usr=User.objects.get(username=em)
			return render(request,"usignup.html",{"msg":"user already registered"})
		except User.DoesNotExist:
			pw = ""
			text = "123456789"
			for i in range(4):
				pw = pw + text[randrange(len(text))]
			print(pw)
			subject = "Welcome to Task Master Web App"
			msg = "Ur password is " + str(pw)
			send_mail(subject, msg, EMAIL_HOST_USER, [str(em)])
			usr=User.objects.create_user(username=em,password=pw)
			usr.save()
			return redirect("ulogin")
	else:
		return render(request,"usignup.html")

def ulogin(request):
	if request.method=="POST":
		em=request.POST.get("em")
		pw=request.POST.get("pw")
		usr=authenticate(username=em,password=pw)
		if usr is not None:
			login(request,usr)
			return redirect("home")
		else:
			return render(request,"ulogin.html",{"msg":"invalid login"})
	else:
		return render(request,"ulogin.html")

def ulogout(request):
	logout(request)
	return redirect("ulogin")


# authentication part(closed)
def add_task(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        form = TaskAppForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            task = form.save(commit=False)
            task.user = user
            task.save()
            print(task)
            return redirect('home')
        else:
            return render(request, 'add_task.html', {'form': form})
    else:
         return redirect('ulogin')

def view_task(request):
    if request.user.is_authenticated:
        user = request.user
        form = TaskAppForm()
        tasks = TaskApp.objects.filter(user=user).order_by('priority')
        return render(request, 'view_task.html', {'form': form, 'tasks': tasks})
    else:
        return redirect('ulogin')


def delete_task(request, id):
    print(id)
    TaskApp.objects.get(pk=id).delete()
    return redirect('view_task')


def change_status(request, id, status):
    dd = TaskApp.objects.get(pk=id)
    dd.status = status
    dd.save()
    return redirect('view_task')

def info1(request):
	return render(request, 'info1.html')

def user_cp(request):
	if request.method == "POST" and request.user.is_authenticated:
		em = request.user.username
		pw1 = request.POST.get("pw1")
		pw2 = request.POST.get("pw2")
		if pw1 == pw2:
			usr = User.objects.get(username=em)
			usr.set_password(pw1)
			usr.save()
			return redirect("ulogin")
		else:
			return render(request, "user_cp.html", {"msg":"password did not match"})
	elif request.method == "GET" and request.user.is_authenticated:
		return render(request, "user_cp.html")
	else:
		return redirect("ulogin")
