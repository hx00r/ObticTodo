from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from util import mongoClient # mongo client i have written

def login(request):
    if request.method == 'POST':
        if 'login_stage' in request.POST:
            user_name = request.POST['user_inp']
            pass_inp = request.POST['pass_inp']
            user = auth.authenticate(username=user_name, password=pass_inp) # this orm will auth the user (check if it's correct)
            if user is not None: # if user is exist we will keep going on auth him
                auth.login(request, user) # the log in code that takes the 'user' 
                return redirect('index')
            else: # if wrong username or password or unfound user this else will return
                messages.info(request, 'Wrong username/password')
                return redirect('index')
    return render(request, 'login.html')

def regitser(request):
    if request.method == 'POST':  # this will check if the incoming request is post or not
        first_nameGT = request.POST['frst_name']
        last_nameGT = request.POST['last_name']
        user_inp = request.POST['user_inp']
        email_inp = request.POST['email_inp']
        pass_inp1 = request.POST['pass_inp1']
        pass_inp2 = request.POST['pass_inp2']
        if len(first_nameGT) == 0 and len(last_nameGT) == 0 and len(user_inp) == 0 and len(email_inp) == 0 and len(pass_inp1) == 0 and len(pass_inp2) == 0:
            messages.info(request, "You can't leave all fields plank")
        elif len(first_nameGT) == 0 or len(last_nameGT) == 0:
            messages.info(request, "Please at least enter firstname or lastname")
        elif len(user_inp) == 0:
            messages.info(request, "Username can not be empty")
        elif len(email_inp) == 0:
            messages.info(request, "E-mail can not be empty")
        elif len(pass_inp1) == 0 and len(pass_inp2) == 0:
            messages.info(request, "Password can not be empty")
        elif pass_inp1 != pass_inp2:
            messages.info(request, "Password didn't match")
        else:
            user_auth = User.objects.create_user(first_name=first_nameGT,
                                                    last_name=last_nameGT,
                                                    username=user_inp,
                                                    email=email_inp,
                                                    password=pass_inp1)  # for the auth table data
           
            user_auth.save()  # this will save the data inside the auth_user table (for auth porpose)
            mongoClient.register_v2(user_auth.id, user_inp)
            # this will clean the register message label
            messages.info(request, 'Registration completed successfully')
            return redirect('index')
    return render(request, 'register.html')

@login_required(login_url='/login')  
def settings(request):
    return render(request, 'settings.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='/login')  
@csrf_exempt
def update_account(request):
    redi = redirect('settings')
    userData = User.objects.get(id = request.user.id)
    if 'updaInfo-stage' in request.POST:
        email_get = request.POST.get('emailINP')
        if email_get == userData.email:
            messages.error(request, 'E-Mail is the same as old E-Mail')
            return redi
        if len(email_get) == 0:
            messages.error(request, 'E-Mail can not be blank!')
            return redi
        else:
            User.objects.update(email = email_get)
            messages.success(request, 'E-Mail has been updated successfully')
            return redi
    if 'updatePassword-stage' in request.POST:
        old_password = request.POST.get('oldPassINP')
        newPassword = request.POST.get('NewPassINP')
        RenewPassword = request.POST.get('ReNewPassINP')
        if userData.check_password(old_password):
            if newPassword == RenewPassword:
                if len(newPassword) < 6:
                    messages.error(request, 'You need stronger Password')
                else:
                    newPassword_hash = make_password(newPassword)
                    User.objects.update(password = newPassword_hash)
                    messages.success(request, 'Password has been changed successfully')
            else:
                messages.error(request, 'Passwords did not match')

        else:
            messages.error(request, 'Old password is wrong')
    if 'del-acc-verfStage' in request.POST:
        userData.delete()
        mongoClient.delteAccount(request.user.id)
        messages.info(request, 'Account has been deleted successfully! you will no longer be able to use this account anymore')
        auth.logout(request)
        return redirect('login')
    return redi