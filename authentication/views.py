from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.utils.http import url_has_allowed_host_and_scheme
from django.shortcuts import redirect
from django.contrib import messages
from .forms import RegistrationForm

# Create your views here.
def log_in(request):
    if request.method == "POST":
        # print(request.GET["next"])
        print(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]

        # Check if user exists
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect_after_login(request)
        else:
            messages.error(request, "Invalid username or password.")
            return redirect(".")

    return render(request, 'registration/login.html')

def redirect_after_login(request):
    nxt = request.GET.get("next", None)
    if nxt is None:
        return redirect("/")
    elif not url_has_allowed_host_and_scheme(
        url=nxt,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect("/")
    else:
        return redirect(nxt)

def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    
    return render(request, 'registration/signup.html')