from django import forms
from . models import Custom_user
import re

class SignupForm(forms.ModelForm):

    password = forms.CharField(
        label="Password",
        widget= forms.PasswordInput(attrs={
            'class':'form-input',
            'placeholder':'Enter Password'
        })
    )

    confirm_password = forms.CharField(
        label = "Confirm Password",
        widget= forms.PasswordInput(attrs={
            'class':'form-input',
            'placeholder':'Confirm password'
        })
    )

    class Meta:
        model = Custom_user
        fields = ['username','email','password']

        widgets = {
            'username':forms.TextInput(attrs={
                'class':'form-input',
                'placeholder':'Enter username'
            }),
            'email':forms.EmailInput(attrs={
                'class':'form-input',
                'placeholder':'Enter email'
            }),
        }
    
    def clean_username(self):
        username = self.cleaned_data.get('username').strip()
    

        if username and len(username) < 5:
            raise forms.ValidationError("Username must be at least 5 Characters")
        
        if Custom_user.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken")       
        
        return username
    

    
    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 Charaters")
        if not re.search(r"[A-Z]",password):
            raise forms.ValidationError("Password must contain a upper case")
        if not re.search(r"[a-z]",password):
            raise forms.ValidationError('Password must contain a lower case')
        if not re.search(r"[0-9]",password):
            raise forms.ValidationError("password must contain a digit")
        return password
    


    def clean_email(self):
        email = self.cleaned_data.get('email').strip().lower()
        blocked = ['admin@gmail.com','test@gmail.com']
        if Custom_user.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")
        if not email.endswith("@gmail.com"):
            raise forms.ValidationError("Only Gmail address are allowed")
        if email in blocked:
            raise forms.ValidationError("This email is not allowed")
        return email
        

        

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')


        if  password != confirm_password:
            raise forms.ValidationError("password do not match")
        
        return cleaned_data
    
    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user