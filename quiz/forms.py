from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Subject, Question, Choice

# Registration form
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

#from django import forms
from .models import Question, Choice

class QuizForm(forms.Form):
    def __init__(self, *args, subject_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if subject_id:
            questions = Question.objects.filter(subject_id=subject_id).prefetch_related('choices')
            for question in questions:
                choices = [(choice.id, choice.text) for choice in question.choices.all()]
                self.fields[f'question_{question.id}'] = forms.ChoiceField(
                    label=question.text,
                    choices=choices,
                    widget=forms.RadioSelect,
                    required=True
                )
