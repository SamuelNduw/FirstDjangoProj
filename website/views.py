from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

def home(request):
    records = Record.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have been successfully Logged In")
                return redirect('home')
            else:
                messages.error(request, "There was an error logging you in, please try again!")
        else:
            messages.error(request, "Username and password are required!")

        return redirect('home')
    
    return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been Logged Out")
    return redirect('home')

def register(request):
    if request.method == 'POST' :
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authentication and Login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have been Successfully Registered! Welcome!")
                return redirect('home')
        else:
            messages.error(request, "There was an error with your registration. Please check the details and try again.")
    else:
        form = SignUpForm()
        
    return render(request, 'register.html', {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, "You must be Logged In to access that page")
        return redirect('home')
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        customer_record.delete()
        messages.success(request, "You have successfully deleted the record!")
        return redirect('home')
    else:
        messages.error(request, "You must be Logged In to delete a record.")

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Successfully Added.")
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.error(request, "You must be Authenticated to perform this action!")
        return redirect('home')
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Updated Successfully")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.error(request, "You must be Logged In to do this action")
        return redirect('home')