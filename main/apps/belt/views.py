from django.shortcuts import render, redirect
from django.contrib import messages
from models import *
import bcrypt

# Create your views here.


def index(request):
    if 'current_user' not in request.session:
        request.session['current_user'] = 0
    if 'trip_id' not in request.session:
        request.session['trip_id'] = 0
    return render(request, "belt_temp/index.html")

def register(request):
    errors = user.objects.registration_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
            print errors.iteritems()
        return redirect('/')
    else:
        print request.POST['name']
        password = request.POST['password']
        pwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt(8))
        user.objects.create(name=request.POST['name'], username=request.POST['username'], password=pwd)
        user_name = request.POST['username']
        request.session['current_user'] = request.POST['username']
        query = user.objects.get(username=user_name)
        print query
        return redirect('/main')


def signIn(request):
    errors = user.objects.login_validator(request.POST)
    if len(errors):
        print errors
        for tag, error in errors.iteritems():
            print errors.iteritems()
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        user_name = request.POST['username']
        password = request.POST['password']
        query = user.objects.get(username=user_name)
        print query.id
        pwd = bcrypt.hashpw(password.encode(), query.password.encode())
        #checks password
        if pwd == query.password:
            request.session['current_user'] = request.POST['username']
            return redirect("/main")
        else:
            messages.error(request, 'Invalid username or password')
    return redirect("/")

def main(request):
    user_id = user.objects.get(username=request.session['current_user'])
    t1 = trip.users
    user_trips = trip.objects.filter(users__id=user_id.id)    
    
    print user_trips
    context = {
        "user": user_id,
        "user_trips": user_trips,
        "trips": trip.objects.exclude(users=user_id),
    }
    print user
    return render(request, 'belt_temp/main.html', context)

def join(request, num):
    request.session['trip_id'] = num
    user_id = user.objects.get(username=request.session['current_user'])
    add_new = trip.objects.get(id=num)
    add_new.users.add(user_id)
    return redirect("/main")

def add_trip(request, num):
    request.session['trip_id'] = num
    return render(request, "belt_temp/add_trip.html")

def added(request):
    errors = user.objects.trip_validator(request.POST)
    print errors
    if len(errors):
        print errors
        for tag, error in errors.iteritems():
            print errors.iteritems()
            messages.error(request, error, extra_tags=tag)
        return redirect('/main')
    else:
        user_id = user.objects.get(username=request.session['current_user'])
        u1 = user.objects.get(id=user_id.id)
        trip1 = trip.objects.create(destination=request.POST["dest"], plan=request.POST['plan'], start=request.POST['start_date'], end=request.POST['end_date'], creator=user_id)
        trip1.users.add(u1)
    return redirect("/main")

def destination(request, num):
    # print trip.objects.filter(id=3)
    # user_trips = trip.objects.filter(id=num) 
    # print user_trips.trips.all()
    user_id = user.objects.get(username=request.session['current_user'])
    add_new = trip.objects.get(id=num)
    all = trip.objects.filter(id=num)
    print add_new.creator.name
    print add_new.users.exclude(name=add_new.creator.name)
    context = {
        "trips": trip.objects.filter(id=num),
        "group": add_new.users.exclude(name=add_new.creator.name),
        "leader": add_new.creator,
    }
    return render(request, "belt_temp/destination.html", context)

def signOut(request):
    request.session.clear()
    return redirect('/')
