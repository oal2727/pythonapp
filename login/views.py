from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse,HttpResponseRedirect
from .forms import UsuarioRawForm,UsuarioLoginForm
from django.contrib.auth import authenticate
from .models import Usuario
from django.contrib import messages
import bcrypt
# Create your views here.
#form cleaned_data is array
#form normal = objects.create_user() #user.save()

#cleaned_Data => retorna objeto

#Model.objects.create  => 
#Model.objects.filter => return []
#cleaned_data => {'nombre': 'qwegfd', 'apellido': 'dfgdfg', 'usuario': 'gfdgdfg', 'password': '123'}

def Index(request):
    return render(request,"index.html",{})

#falta el tema de encryptacion , deploy github con unicorn fin .. 
#ver el tema de administracion global ... 

#we need encrypt password
class Register(View):
    template_name = "register.html"
    def get(self,request):
        form = UsuarioRawForm()
        context = {"form":form}
        return render(request,self.template_name,context)
    def post(self,request):
        form = UsuarioRawForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data["usuario"]
            password = form.cleaned_data["password"]
            password1 = form.cleaned_data["password1"]
            if password == password1:
                if Usuario.objects.filter(usuario=usuario).exists():
                    messages.info(request, "User already exists")
                    return redirect("/register")
                else:
                    form.cleaned_data.pop("password1",None)
                    hash = make_password_hash(password)
                    form.cleaned_data["password"]=hash
                    Usuario.objects.create(**form.cleaned_data)
                    return HttpResponseRedirect("/login")
            else:
                messages.info(request, "Password not maching")
                return redirect("/register")



class Login(View):
    template_name = "login.html"
    def get(self,request):
        form = UsuarioRawForm()
        context = {"form":form}
        return render(request,self.template_name,context)
    #The view login.views.Login didn't return an HttpResponse object. It returned None instead. => problema de objeto
    def post(self,request):
        #tomaba en cuenta todo el form y solo requiero de 2 
        form = UsuarioLoginForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data["usuario"]
            password = form.cleaned_data["password"]
            user = Usuario.objects.filter(usuario=usuario).values()
            if(user):
                userverify=[]
                for usuarios in user:
                    verify = is_password_valid(password,usuarios["password"])
                    if verify: 
                        request.session["usuarioid"] = usuarios["id"]
                        return HttpResponseRedirect("/welcome")
                    else:
                        messages.info(request, "Password don't exists")
                        return redirect("/login")
            else:
                messages.info(request, "User don't exists.")
                return redirect("/login")
           
class Logout(View):
    def get(self,request):
        try:
            print("delete sesion")
            del request.session['usuarioid']
        except KeyError:
            pass
        return redirect("/")

class Welcome(View):
    template_name="welcome.html"
    def get(self,request):
        if 'usuarioid' in request.session:
            userid = request.session["usuarioid"]
            usuario = Usuario.objects.filter(id=userid)
            return render(request,self.template_name,{"data":usuario})
            return redirect("/")
        else:
            return redirect("/")
       

def make_password_hash(password):
    hash = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt())
    return hash.decode('utf-8')

def is_password_valid(password,passwordhash):
    return bcrypt.checkpw(password.encode('utf-8'), passwordhash.encode('utf-8'))