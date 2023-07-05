
from django.shortcuts import render,redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView 
from .forms import EmailAuthenticationForm

# Create your views here.

def activate_email(request,user,to_email):
    mail_subject = "Activate your user account"
    message = render_to_string('accounts/activate_account.html',
                               {
                                'domain':get_current_site(request).domain,
                                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                'token': account_activation_token.make_token(user),
                                'protocol': 'https' if request.is_secure() else 'http'
                                })
    
    email = EmailMessage(mail_subject,message,to=[to_email])
    
    if email.send():
        messages.success(request,f'Kindly check your inbox at {to_email} to activate your account ')
    else:
        messages.error(request,f'Problem sending email to {to_email}, please check your email and try again ')
               

def activate(request,uidb64,token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save() 
        
        messages.success(request,f'Thank you for confirming your email, You may now login')
        return redirect('login')
        
    else:
        messages.error(request,f'Activation link is invalid')
    return redirect('home') 
    
def signup_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_active =False
            new_user.save()
            # username = form.cleaned_data.get("username")
            
            # messages.success(request,f'Account successfully created for {username}!, You can login into your account now')
            activate_email(request,new_user,form.cleaned_data.get('email'))
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    
    