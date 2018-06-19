from django.contrib.auth import authenticate, login, get_user_model,logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.views.generic import CreateView, FormView
from .forms import ContactForm, LoginForm, RegisterForm

def home_page(request):
    name = "new user"
    if request.user.is_authenticated():
        name = request.user.name
    context = {
        "title":"Hello World!",
        "content":" Welcome to the homepage.",
        "name": name

    }
    if request.user.is_authenticated():
        context["premium_content"] = "YEAHHHHHH"
    return render(request, "home_page.html", context)

def about_page(request):
    context = {
        "title":"About Page",
        "content":" Welcome to the about page."
    }
    return render(request, "home_page.html", context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title":"Contact",
        "content":" Welcome to the contact page.",
        "form": contact_form
    }
    if contact_form.is_valid():
        if request.is_ajax():
            return JsonResponse({"message":"Thankyou"})

    return render(request, "contact/view.html", context)


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    # print("User logged in")
    #print(request.user.is_authenticated())
    if form.is_valid():
        print(form.cleaned_data)
        username  = form.cleaned_data.get("username")
        password  = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        print(user)
        #print(request.user.is_authenticated())
        if user is not None:
            #print(request.user.is_authenticated())
            login(request, user)
            # Redirect to a success page.
            #context['form'] = LoginForm()
            return redirect("/")
        else:
            # Return an 'invalid login' error message.
            print("Error")

    return render(request, "auth/login.html", context)

def logout_page(request):

    logout(request)
    return redirect("/")



class RegisterView(CreateView):
        form_class = RegisterForm
        template_name = "register.html"
        success_url = '/register/'
