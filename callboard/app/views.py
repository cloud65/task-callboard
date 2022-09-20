from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.models import User
from .models import *
from .forms import *
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
    return render(request=request, template_name="registration/register.html",
                  context={"form": form, 'data': request.POST})


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
    context_object_name = 'data'
    paginate_by = 6


def announcement_detail(request, pk, action):
    announcement = Announcement.objects.get(pk=pk) if pk!=0 else None
    init_recall = {'announcement': pk, 'user': request.user}
    recall_form = RecallFormModel(initial=init_recall) if not announcement is None else None

    form = None
    if action == 'edit' and request.user==announcement.user:
        form = AnnouncementFormModel(instance=announcement)
    elif action == 'add':
        form = AnnouncementFormModel(initial={'user': request.user})

    if request.method == "POST" and request.user.is_authenticated:
        if request.POST.get('type') == 'comment':
            recall_form = RecallFormModel(request.POST)
            if recall_form.is_valid():
                recall_form.save()
                recall_form = RecallFormModel(initial=init_recall)
        elif request.POST.get('type') == 'post':
            if action == 'add':
                form = AnnouncementFormModel(request.POST)
            else:
                form = AnnouncementFormModel(request.POST, instance=announcement)
            if form.is_valid():
                form.save()
                return redirect(f"/post/{form.instance.pk}/detail")

    return render(request, 'app/post.html', {'form': form, 'comment_form': recall_form, 'data': announcement})
