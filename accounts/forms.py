from django import forms
from .models import User , UserProfile
from .validators import allow_only_images

class UserForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder':'Qwerty@123'
    }))
    confirm_password = forms.CharField(widget= forms.PasswordInput(attrs={
        'placeholder':'Confirm password'
    }))
    phone_number = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'username' , 'email' , 'phone_number' , 'password']
    def __init__(self , *args , **kwargs):
        super(UserForm , self).__init__(*args ,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['style'] = 'width:90%'
            self.fields[field].widget.attrs['class'] = 'form-control fs-6'
     
    def clean(self):
        cleaned_data = super(UserForm , self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start Typing...' , 'required':'required'}))
    profile_picture = forms.FileField(validators=[allow_only_images])
    cover_picture = forms.FileField(validators=[allow_only_images])
    class Meta:
        model = UserProfile
        fields = ['profile_picture' , 'cover_picture' , 'address',  'state' , 'city' ,'latitude' , 'longitude' , ]
    def __init__(self , *args , **kwargs):
        super(UserProfileForm ,self).__init__(*args , **kwargs)
        self.fields['latitude'].widget.attrs['readonly']= True
        self.fields['longitude'].widget.attrs['readonly']= True