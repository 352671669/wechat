from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
# Create your views here.
from .models import WeChatUser, Status, settings, Reply


def home(request):
    return render(request, "homepage.html")


@login_required
def show_user(request):
    po = WeChatUser.objects.get(user=request.user)
    return render(request, "user.html", {"user": po})


@login_required
def show_status(request):
    statuses = Status.objects.all()
    for status in statuses:
        status.likes = Reply.objects.filter(status=status, type="0")
        status.comments  =Reply.objects.filter(status=status, type="1")
    return render(request, "status.html", {"statuses": statuses})


@login_required
def submit_post(request):
    user = WeChatUser.objects.get(user=request.user)
    text = request.POST.get("text")
    uploaded_file = request.FILES.get("pics")

    if uploaded_file:
        name = uploaded_file.name
        with open("./moments/static/image/{}".format(name), 'wb') as handler:
            for block in uploaded_file.chunks():
                handler.write(block)
    else:
        name = ''


    if text:
        status = Status(user=user, text=text, pics=name)
        status.save()
        return redirect("/status")

    return render(request, "my_post.html")


def register(request):
    try:
        username, password, email = [request.POST.get(key) for key in ("username", "password", "email")]

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        WeChatUser.objects.create(user=user)
    except Exception as err:
        result = False
        message = str(err)
    else:
        result = True
        message = "Register success"
    return JsonResponse({'result': result, 'message': message})


@login_required
def update_user(request):
    try:
        kwargs = {key:request.POST.get(key) for key in ("motto", "region", "pic") if request.POST.get(key)}
        WeChatUser.objects.filter(user=request.user).update(**kwargs)

        email = request.POST.get("email")
        if email:
            dj_user = User.objects.get(username=request.user.username)
            dj_user.email = email
            dj_user.save()

    except Exception as err:
        result = False
        message = str(err)
    else:
        result = True
        message = "Update success"
    return JsonResponse({'result': result, 'message': message})