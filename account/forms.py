
from django import forms


from account.models import CustomUser, UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password'
    }))
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'year_of_birth','phone_no', 'password']
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter Firstname'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Lastname'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email e.g abc@example.com'
        self.fields['phone_no'].widget.attrs['placeholder'] = 'Telephone'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            
    def clean(self):
        clean_data = super(RegistrationForm, self).clean()
        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )
            
            
class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_no']
        
        
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        
            
class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages= {'invalid':("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture']
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'