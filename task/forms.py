
from django import forms
from task.models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [ 'description', 'due_date']  