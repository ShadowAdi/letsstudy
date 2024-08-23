from django.shortcuts import render, redirect
from .models import Room, Topic, Message,User
from .forms import RoomForm, UserForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import MyUserCreationForm

def loginPage(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("Home")

    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User Does Not Exist.")
            return render(request, "base/login_register.html", {"page": page})

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("Home")
        else:
            messages.error(request, "Credentials Don't Match.")
            return render(request, "base/login_register.html", {"page": page})

    context = {"page": page}
    return render(request, "base/login_register.html", context)


def registerUser(request):
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request=request, user=user)
            return redirect("Home")
        else:
            messages.error(request, "An Error Occured During Registration")

    return render(
        request=request,
        template_name="base/login_register.html",
        context={"form": form},
    )


def logoutUser(request):
    logout(request)
    return redirect("Home")


def Home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    queryItem = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    topics = Topic.objects.all()[0:5]
    room_count = queryItem.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    return render(
        request,
        "base/home.html",
        {
            "rooms": queryItem,
            "topics": topics,
            "RoomCount": room_count,
            "roomMessages": room_messages,
        },
    )


def RoomView(request, pk):
    room = Room.objects.get(id=pk)
    roomMessages = room.message_set.all()
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("room", pk=room.id)

    context = {"room": room, "roomMessages": roomMessages, "participants": participants}
    return render(request, "base/Room.html", context)


@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )

        return redirect("Home")
    context = {"form": form, "topics": topics}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("You are Not allowed!!!")
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get("name")
        room.topic = topic
        room.description = request.POST.get("description")
        room.save()
        return redirect("Home")
    context = {"form": form, "topics": topics, "room": room}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are Not allowed!!!")
    if request.method == "POST":
        room.delete()
        return redirect("Home")
    return render(request, "base/delete-form.html", {"obj": room})


@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        return HttpResponse("You are Not allowed!!!")
    if request.method == "POST":
        message.delete()
        return redirect("Home")
    return render(request, "base/delete-form.html", {"obj": message})


@login_required(login_url="login")
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {
        "user": user,
        "rooms": rooms,
        "roomMessages": room_messages,
        "topics": topics,
    }
    return render(
        request=request, template_name="base/userProfile.html", context=context
    )


@login_required(login_url="login")
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile", pk=user.id)

    return render(
        request=request, template_name="base/edit-user.html", context={"form": form}
    )


def topicsPage(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    topics = Topic.objects.filter(name__icontains=q)
    return render(
        request=request, template_name="base/topics.html", context={"topics": topics}
    )


def activitiesPage(request):
    room_messages=Message.objects.all()

    return render(request=request, template_name="base/activity.html", context={"roomMessages":room_messages})
