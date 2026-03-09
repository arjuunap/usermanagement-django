from django import forms
from . models import Custom_user


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
        username = self.cleaned_data.get('username')

        if len(username) < 5:
            raise forms.ValidationError("Usename must be at least 5 Characters")
        
        return username
    
    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 Charaters")
        
        return password
    
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')


        if password != confirm_password:
            raise forms.ValidationError("password do not match")
        
        return cleaned_data
    
    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user