from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import *
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        questions = QuesModel.objects.order_by('?')[:5]
        if request.method == "POST":
            print(request.POST)
            # questions = QuesModel.objects.all()
            score = 0
            wrong = 0
            correct = 0
            total = 0
            for q in questions:
                total += 1
                print(request.POST.get(q.question))
                print(q.ans)
                print()
                if q.ans == request.POST.get(q.question):
                    score += 10
                    correct += 1
                else:
                    wrong += 1
            percent = score / (total * 10) * 100
            context = {
                "score": score,
                "time": request.POST.get("timer"),
                "correct": correct,
                "wrong": wrong,
                "percent": percent,
                "total": total,
            }
            return render(request, "Quiz/result.html", context)
        else:
            # questions = QuesModel.objects.order_by('?')[:5]
            context = {"questions": questions}
            return render(request, "Quiz/quiz.html", context)
    else:
        return render(request,"Quiz/home.html")

@login_required
def addQuestion(request):
    if request.user.is_staff:
        form = addQuestionform()
        if request.method == "POST":
            form = addQuestionform(request.POST)
            if form.is_valid():
                form.save()
                return redirect("/")
        context = {"form": form}
        return render(request, "Quiz/addQuestion.html", context)
    else:
        return redirect("home")


class registerPage(View):
    def get(self, request):
        form = createuserform()
        return render(request, "Quiz/register.html", {"form": form})

    def post(self, request):
        form = createuserform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "congratulations! Registred successfully!!")
        return render(request, "Quiz/register.html", {"form": form})



def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.warning(request, "Username or Password incorrect!!")
                return render(request, "Quiz/login.html")
        context = {}
        return render(request, "Quiz/login.html", context)

@login_required
def logoutPage(request):
    logout(request)
    return redirect("/")
