from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML,\
                                ButtonHolder, Submit

from .custom_layout import *
from .models import Company, Question, Choice
from .helper import language_check


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = '__all__'


class CreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

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
                Field('company'),
                Field('pub_date'),
                Fieldset('Add choices', Formset('choices')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Add Question')),
                )
            )
    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     print(cleaned_data)
        # choice_text = cleaned_data['choice_text']
        # value = language_check(choice_text)
        # if value[0]:
        #     print('hotnaohsntho')
        #     self.add_error('choice_text', value[1])
            # raise forms.ValidationError(
            #         'Coarse words like ' + value[1] + ' are not allowed.')

ChoiceFormSet = forms.inlineformset_factory(Question,
                                            Choice,
                                            form=ChoiceForm,
                                            fields=['choice_text'],
                                            extra=3)
