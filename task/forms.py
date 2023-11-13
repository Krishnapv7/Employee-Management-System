from django import forms 
from .models import Task
from django.forms import DateInput
from user.models import BaseUser



class TaskForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        assigned = cleaned_data.get('assigned')

        # Check if assigned is None or empty string
        if assigned in (None, ''):
            cleaned_data['assigned'] = None  # Set assigned to None
        return cleaned_data
   
    class Meta:
        model = Task
        fields = ['title','description','date','status','assigned']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),    
        }
        
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['status'].empty_label = None
        self.fields['assigned'].empty_label = None
        
        
class TaskFilterForm(forms.Form):
    title = forms.CharField(required=False)
    status = forms.ChoiceField(choices=Task.STATUS_CHOICE,required=False)
    assigned = forms.ModelChoiceField(queryset=BaseUser.objects.all(),required=False)
    