from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
# Create your views here.
def home(request):
    if 'user' in request.session:
        return redirect('/dashboard')
    else:
        return redirect('/login')
def login(request):
    if "user" in request.session:
        return redirect('/dashboard')
    return render(request, 'login.html')
def login_form(request):
    if request.method=="POST":
        user=Users.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user'] = logged_user.id
                messages.success(request,"Successfully logged in")
                return redirect("/dashboard")
            else:
                messages.error(request,"Email or password is not correct")
                return redirect("/login")
        else:
            messages.error(request,"Email or password is not correct")
            return redirect("/")
def register(request):
    if 'user' in request.session:
        return redirect("/dashboard")
    if 'errors' in request.session:
        return render(request,'register.html', {'errors': request.session['errors']})
    else:
        request.session['errors'] = {}
        return redirect("/register")
   

def register_form(request):
    errors = Users.objects.validator(request.POST)
    if len(errors)>0:
        request.session['errors'] = errors
        for key,val in errors.items():
            messages.error(request,val)
        return redirect("/register")
    else:
        if request.method=="POST":
            password=request.POST['password']
            passHash=bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()
            newUser = Users.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],
            password=passHash)
            request.session['user'] = newUser.id
            del request.session['errors']
            messages.success(request,"User successfully created")
        return redirect("/dashboard")
def dashboard(request):
    if 'user' in request.session:
        user = Users.objects.filter(id=request.session['user'])
        trips = Trip.objects.all()
        return render(request, 'dashboard.html',{'user':user[0], 'trips': trips})
    else:
        return redirect("/login")

def logout(request):
    if 'user' in request.session:
        request.session.flush()
        return redirect('/login')
    else:
        return redirect("/dashboard")

def new_trip(request):
    if 'user' in request.session:
        user  = Users.objects.get(id=request.session['user'])
        return render(request, 'new_trip.html', {'user':user})
    else:
        return render(request, 'new_trip.html')
def new_trip_form(request):
    errors = Trip.objects.validator(request.POST)
    print(errors)
    if len(errors)>0:
        for key,val in errors.items():
            messages.error(request,val)
        return redirect("/trips/new")
    else:
        if request.method == 'POST':
            user = Users.objects.get(id=request.session['user'])
            Trip.objects.create(destination=request.POST['destination'],start_date=request.POST['start_date'],
            end_date=request.POST['end_date'], plan=request.POST['plan'], created_by=user
            )
        return redirect('dashboard')

def get_trip(request, id):
    trip = Trip.objects.get(id=id)
    user = Users.objects.get(id=request.session['user'])
    return render(request,'get_trip.html', {'trip':trip, 'user':user})  

def edit_trip(request, id):
    if 'user' in request.session:
        trip = Trip.objects.get(id=id)
        user = Users.objects.get(id=request.session['user'])
        return render(request,'edit_trip.html',{'trip':trip,'user':user})
    else:
        return redirect('/dashboard')
def update_trip_form(request, id):
    errors = Trip.objects.validator(request.POST)
    print(errors)
    if len(errors)>0:
        for key,val in errors.items():
            messages.error(request,val)
        return redirect(f"trips/edit/{id}")
    else:
        trip = Trip.objects.get(id=id)
        trip.destination = request.POST['destination']
        trip.start_date = request.POST['start_date']
        trip.end_date = request.POST['end_date']
        trip.plan = request.POST['plan']
        trip.save()
        return redirect(f'/trips/{trip.id}')
def remove_trip(request, id):
    user = Users.objects.get(id=request.session['user'])
    trip = Trip.objects.get(id=id)
    if user.id == trip.created_by.id:
        trip.delete()
        return redirect('/dashboard')
    else:
        return redirect('/dashboard')

def join_trip(request, id):
    trip = Trip.objects.get(id=id)
    user = Users.objects.get(id=request.session['user'])
    trip.users_who_join_trip.add(user)
    return redirect('/dashboard')
def cancel_trip(request, id):
    trip = Trip.objects.get(id=id)
    user = Users.objects.get(id=request.session['user'])
    trip.users_who_join_trip.remove(user)
    return redirect('/dashboard')
    
