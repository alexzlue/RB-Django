from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML,\
                                ButtonHolder, Submit

from .custom_layout import *
from .models import Company, Question, Choice
from .helper import language_filter

CHOICE_FORM_SET = forms.inlineformset_factory(Question,
                                              Choice,
                                              form=ChoiceForm,
                                              fields=['choice_text'],
                                              extra=3)


class ChoiceForm(forms.ModelForm):
    ''' Form for choices '''
    class Meta:
        model = Choice
        fields = '__all__'

    def clean_choice_text(self):
        language_filter(self.cleaned_data['choice_text'])
        return self.cleaned_data['choice_text']


class CreateForm(forms.ModelForm):
    ''' Form that will iclude formset to create question'''
    company = forms.CharField()

    class Meta:
        model = Question
        fields = ['question_text', 'company']

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
                Field('company', id='autocomplete'),
                Fieldset('Add choices', Formset('choices')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Add Question')),
            )
        )

    def clean_company(self):
        name = self.cleaned_data['company']
        try:
            return Company.objects.get(name=name)
        except Company.DoesNotExist:
            raise forms.ValidationError(str(name) + " is an invalid company")

    def clean_question_text(self):
        language_filter(self.cleaned_data['question_text'])
        return self.cleaned_data['question_text']
