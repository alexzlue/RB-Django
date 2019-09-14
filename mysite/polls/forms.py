from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML,\
                                ButtonHolder, Submit

from .custom_layout import *
from .models import Company, Question, Choice
from .helper import language_check
from django.utils.translation import gettext_lazy as _


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = '__all__'


class CreateForm(forms.ModelForm):
    company = forms.CharField(max_length=200)

    class Meta:
        model = Question
        fields = ['question_text', 'pub_date']
        widgets = {
            'pub_date': forms.SelectDateWidget()
        }

    def __init__(self, *args, **kwargs):
        '''
        adapted code from:
        https://dev.to/zxenia/django-inline-formsets-with-class-based-views-and-crispy-forms-14o6
        '''
        super(CreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('question_text'),
                Field('company', id='txtSearch'),
                Field('pub_date'),
                Fieldset('Add choices', Formset('choices')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Add Question')),
            )
        )

    def clean(self):
        cleaned_data = super().clean()
        company = cleaned_data['company']
        try:
            # print(type(Company.objects.get(name=company)))
            co = Company.objects.get(name=company)
            print(co.name)
            # raise forms.ValidationError(str(co) + ' exists!')
        except:
            raise forms.ValidationError(company + " is not a valid company.")
        # cleaned_data['company'] = co.id
        # print('haonestuh')


ChoiceFormSet = forms.inlineformset_factory(Question,
                                            Choice,
                                            form=ChoiceForm,
                                            fields=['choice_text'],
                                            extra=3)
