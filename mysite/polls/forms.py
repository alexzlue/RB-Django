from django import forms

from .models import Company, Question, Choice


class CreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
    # question = forms.CharField(label='Question', max_length=200)
    # company = forms.CharField(label='Company', max_length=50)
