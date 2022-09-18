from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import *
from .forms import NewUserForm
from .email import *


def register_request(request):  # Регистрация и отправка кода
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_email_code(user)
            return redirect(f"/register/email/{user.pk}")
    else:
        form = NewUserForm()
    return render(request=request, template_name="registration/register.html", context={"form": form, 'data': request.POST})


def register_email_request(request, user_id):  # Проверка кода Email
    data = {'user': user_id}
    if request.method == "POST":
        codes = EmailCodes.objects.filter(user=user_id).first()
        if codes and request.POST['code'].strip() == codes.code:
            user = codes.user
            user.is_active = True
            user.save()
            return redirect(f"/accounts/login?username={user.username}")
        data['error'] = 'Неверный код'
    return render(request=request, template_name="registration/email.html", context={"data": data})


def register_email_request_resend(request, user_id):  # Повторная отправка кода Email
    print([u.id for u in User.objects.all()])
    user = User.objects.filter(id=int(user_id)).first()
    if user:
        send_email_code(user)
    return redirect(f"/register/email/{user_id}")


class AnnouncementList(ListView):
    model = Announcement
    ordering = '-date_create'
    template_name = 'app/list.html'
    context_object_name = 'posts'
    paginate_by = 6


class AnnouncementDetail(DetailView):
    model = Announcement
    template_name = 'app/post.html'
    context_object_name = 'post'


class AnnouncementCreate(CreateView):
    model = Announcement


class AnnouncementUpdate(UpdateView):
    model = Announcement


class AnnouncementDelete(DeleteView):
    model = Announcement


class RecallList(ListView):
    model = Recall


class RecallCreate(CreateView):
    model = Recall


class RecallUpdate(UpdateView):
    model = Recall


class RecallDelete(DeleteView):
    model = Recall
