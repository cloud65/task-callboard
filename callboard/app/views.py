from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
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
    template_name = 'app/list.html'
    context_object_name = 'data'
    paginate_by = 6

    def get_queryset(self):
        if self.request.path == '/my':
            return Announcement.objects.filter(user=self.request.user).order_by('-date_create')
        elif self.request.path == '/recall':
            return Announcement.objects.filter(
                pk__in=Recall.objects.filter(user=self.request.user).values('announcement')
            ).order_by('-date_create')
        elif self.request.path == '/recall-new':
            return Announcement.objects.filter(
                user=self.request.user,
                pk__in=Recall.objects.filter(is_view=False).values('announcement')
            ).order_by('-date_create')
        else:
            return Announcement.objects.all().order_by('-date_create')


def announcement_detail(request, pk, action):
    prev_url = request.GET.get('prev', '/')
    announcement = Announcement.objects.get(pk=pk) if pk != 0 else None
    init_recall = {'announcement': pk, 'user': request.user}
    recall_form = RecallFormModel(initial=init_recall) if not announcement is None else None

    form = None
    if action == 'edit' and request.user == announcement.user:
        form = AnnouncementFormModel(instance=announcement)
    elif action == 'add' and request.user.is_authenticated:
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
                return redirect(f"/post/{form.instance.pk}/detail?prev={prev_url}")
    elif request.method == "GET" and action == 'del' and request.user == announcement.user:
        announcement.delete()
        return redirect(request.GET.get('redirect', '/'))
    reacll_not_views = [_p['pk'] for _p in announcement.recalls.filter(is_view=False).values('pk')] if announcement else []
    editable = action == 'add' or request.user == announcement.user
    context = {
        'prev': prev_url if prev_url.find('/add') == -1 else '/',
        'form': form,
        'comment_form': recall_form,
        'data': announcement,
        'not_views': reacll_not_views,
        'editable': editable,
        'can_accept': announcement and request.user == announcement.user,
    }
    print(reacll_not_views)
    # Переключим статус в просмотренные
    if request.method == "GET" and announcement and request.user == announcement.user:
        announcement.recalls.filter(is_view=False).update(is_view=True)
    return render(request, 'app/post.html', context)


def accept_comment(request, pk):
    recall = Recall.objects.get(pk=pk)
    if request.user == recall.announcement.user:
        recall.accept = not recall.accept
        recall.save()
    return redirect(request.META.get('HTTP_REFERER'))


class NewsList(ListView):
    model = News
    template_name = 'app/news.html'
    context_object_name = 'data'
    paginate_by = 6
    ordering = ['-date_update']


class NewsDetail(DetailView):
    model = News
    template_name = 'app/news.html'
    context_object_name = 'data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_detail'] = True
        return context
