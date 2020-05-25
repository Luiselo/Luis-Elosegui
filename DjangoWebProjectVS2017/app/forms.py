"""
Definition of forms.
"""

from django import forms
from app.models import User,Pregunta,Respuesta
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class QuestionForm(forms.ModelForm):

        class Meta:
            model = Pregunta
            fields = ('question_text', 'question_tema')

class ChoiceForm(forms.ModelForm):

        class Meta:
            model = Respuesta
            fields = ('choice_text', 'correct',)

class ChoiceForm1(forms.ModelForm):

        class Meta:
            model = Respuesta
            fields = ('choice_text',)

class UserForm(forms.ModelForm):

        class Meta:
            model = User
            fields = ('email','nombre',)

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
class IndexForm(forms.Form):
    type_choices = [(i['question_tema'], i['question_tema']) for i in Pregunta.objects.values('question_tema').distinct()]
    
    Tema = forms.ChoiceField(choices=type_choices)
    