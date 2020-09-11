from django import forms



class UsuarioRawForm(forms.Form):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Input name"}))
    apellido = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Input apellido"}))
    usuario = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Input usuario"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':"Input password"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':"Repeat password"}))


class UsuarioLoginForm(forms.Form):
    usuario = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder':"Input usuario"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':"Input password"}))
