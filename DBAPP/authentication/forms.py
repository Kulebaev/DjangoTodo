from django import forms
from .models import City

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Название города'

    def clean_name(self):
        # Проверяем, что введенный город состоит только из букв
        name = self.cleaned_data['name']
        if not name.isalpha():
            raise forms.ValidationError('Название города должно содержать только буквы.')
        return name
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['comment', 'city', 'user', 'completed']
