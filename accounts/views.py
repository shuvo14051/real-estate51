from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact


def register(request):
    if request.method == 'POST':
        # get from values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # check password match
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "That username is taken")
                return redirect('register')

            if User.objects.filter(email=email).exists():
                messages.error(request, "That email is being used")
                return redirect('register')

            user = User.objects.create_user(
                username=username, email=email, password=password, 
                first_name=first_name, last_name=last_name)

            #login after registrarion
            # auth.login(request, user)
            # messages.success(request, "You are looged in")
            # return redirect('index')

            user.save()
            messages.success(request, "Successfully registerd! You can login now")
            return redirect('login')

        else:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are logged in!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Credintials")
            return redirect('login')


    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, "You are logged out!")

    return redirect('index')


def dashboard(request):
    user_contact = Contact.objects.order_by('-contact_date').filter(user_id = request.user.id)
    context = {
        'contacts': user_contact,
    }
    return render(request, 'accounts/dashboard.html', context)
