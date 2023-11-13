from django import forms
from django.forms import RadioSelect,DateInput
from user.models import BaseUser
from django.contrib.auth.forms import PasswordChangeForm



class UserForm(forms.ModelForm):
    photo = forms.ImageField(required=False)
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
    
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    # password = forms.CharField(label='Password', widget=forms.PasswordInput(render_value=True))
    # confirmpassword = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(render_value=True))
    gender = forms.ChoiceField(widget=RadioSelect, choices=GENDER_CHOICES)
    
    class Meta:
        model = BaseUser
        fields = '__all__'
        
        widgets= {
            'dob' : DateInput(attrs={'type': 'date'}),
            'gender' : RadioSelect,
            
        }
        
        
    # def __init__(self, *args, **kwargs):
    #     super(UserForm, self).__init__(*args, **kwargs)
    #     self.fields['photo'].required = False
    
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirmpassword')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
        
class CustomPasswordChangeForm(PasswordChangeForm):
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False,
        help_text="Enter the same password as above, for verification."
    )        

class UserFilterForm(forms.Form):
    name = forms.CharField(required=False)
    username = forms.CharField(required=False)
    gender = forms.ChoiceField(choices=UserForm.GENDER_CHOICES,required=False)