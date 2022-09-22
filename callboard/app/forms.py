from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_summernote.widgets import SummernoteWidget
from .models import Recall, Announcement


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class AnnouncementFormModel(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "category", "content", "user"]
        widgets = {
            'user': forms.HiddenInput,
            'title': forms.TextInput(attrs={'class': 'input'}),
            'category': forms.Select(attrs={'class': 'input'}),
            'content': SummernoteWidget}
        labels = {'content': 'Текст', 'title': 'Тема', 'category': "Категория"}


class RecallFormModel(forms.ModelForm):
    class Meta:
        model = Recall
        fields = ["content", "announcement", "user"]
        widgets = {
            'user': forms.HiddenInput,
            'announcement': forms.HiddenInput,
            'content': SummernoteWidget}
        labels = {'content': '', }
