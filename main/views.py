from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import models
from datetime import date, timedelta
import json
from .models import *
from .forms import *
from register.forms import RegisterForm
import time
import math

# Create your views here.


@login_required(login_url='/login')
def home(request):
	users = User.objects.all()
	nicknames = nickname.objects.all()
	user_list = []
	for user in users:
		user_nicknames = nickname.objects.filter(user=user)
		if user_nicknames.exists():
			user_nickname = user_nicknames.order_by('?').first()
			user_list.append([user.first_name, user_nickname, user.last_name])
		else:
			user_list.append([user.first_name, 'Someone make me a nickname', user.last_name])


	context = {'users':user_list}
	
	return render(request, "main/home.html", context)


def signup(response):
    return render(response, "main/signup.html", {})

@login_required(login_url='/login')
def athletes(response):
    return render(response, "main/athletes.html", {})

def logout_page(response):
    return render(response, "main/logout_page.html", {})


@login_required(login_url='/login')
def results(request):
	users = User.objects.all()
	today = date.today()
	weekday = today.weekday() # Monday is 0 and Sunday is 6
	filter_start = today - timedelta(days=weekday)

	this_weeks_results = RunTime.objects.filter(date__range = [filter_start, today]) # filter to get results from Monday-today

	start_date = date(2020, 11, 2) #results will be grouped and filtered from this date (must be a Monday!)
	delta = today-start_date
	delta_int = delta.days
	num_weeks = math.ceil(delta_int/7) #round it up

	results_table = []
	for i in range(0,num_weeks):

		dummy_list = []
		added_days = i*7 #add on 7 days, so start date is always a monday
		f_start = start_date + timedelta(added_days)
		f_end = f_start + timedelta(days=6) #add 6 days to start date, i.e. end date is a sunday
		x = RunTime.objects.filter(date__range = [f_start, f_end]).order_by('run_time')
		counter = 0
		for user in users:
			counter+=1
			y = x.filter(user=user) #users results for a given week
			if y.exists():
				best_this_week = y.first()
				dummy_list.append([user, best_this_week.run_time])
			else:
				dummy_list.append([user, 1000])
			if users.count() == counter:
				results_table.append(dummy_list)
			
	
	results_table_sorted = []
	for weekly_result in results_table:
		weekly_result.sort(key=lambda x:x[1])
		results_table_sorted.append(weekly_result)

	
	#block of code to add up the total scores 
	points_tally = []
	for weeks_results in results_table_sorted:
		counter = 0
		for entry in weeks_results: #entry[0] is the user and entry[1] is their best time that week
			counter += 1
			if entry[1] == 1000:
				points_tally.append([entry[0], 0]) #form [user, points that week]
			elif counter == 1:
				points_tally.append([entry[0], 4])
			elif counter == 2:
				points_tally.append([entry[0], 3])
			elif counter == 3:
				points_tally.append([entry[0], 2])
			else:
				points_tally.append([entry[0], 1])

	scores = []
	
	for user in users:
		user_all_results = RunTime.objects.filter(user=user).order_by('run_time')
		user_total_score = 0
		counter = 0

		if user_all_results.exists(): #i.e. the user has submiited a time
			user_weeks_results = this_weeks_results.filter(user=user).order_by('run_time') #sort the list based on run_time
			pb = user_all_results.first().run_time
			total_runs = user_all_results.count()

			if user_weeks_results.exists(): 
				runs_this_week = user_weeks_results.count()
				best_time = user_weeks_results.first().run_time
				
			else:
				best_time = 'No Time Submitted This Week'
				runs_this_week = 0				

			for entry in points_tally:
				counter += 1
				if entry[0] == user:
					user_total_score+=entry[1]
				if counter == len(points_tally):
					scores.append([user, pb, best_time, runs_this_week, total_runs, user_total_score])

		else:
			pb = 'No Times Submitted'
			total_runs = 0
			user_total_score = 0
			runs_this_week = 0
			best_time = 'No Time Submitted This Week'
			scores.append([user, pb, best_time, runs_this_week, total_runs, user_total_score])


	scores.sort(key=lambda x:x[5]) #sort according to total score
	scores.reverse()
	
	titles = []
	values = []
	for entry in scores:
		titles.append(entry[0].username)
		values.append(entry[5])

	json_titles = json.dumps(titles)
	
	current_user = request.user
	context = {'weekly_leaderboard':scores,
	'current_user':current_user,
	'titles':json_titles,
	'my_values':values}
	return render(request, "main/results.html", context)


def cheeky(request):
	return render(request, "main/cheeky.html", {})

def my_results(request, pk):
	Running_Times = RunTime.objects.filter(user=request.user)
	run_num = Running_Times.count()+1
	
	current_user = request.user
	form = TimeForm(initial={'user':request.user, 'title':'Run #'+ str(run_num)}) #initial sets default values for user and title
	
	if request.method == 'POST':
		form = TimeForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data

			if cd['user'] == request.user:
				form.save()
			else:
				return redirect('/cheeky')
		return redirect('/my_results/'+current_user.username)

	context = {'current_user':current_user, 'Running_Times':Running_Times, 'form':form}
	return render(request, "main/my_results.html", context)

def resultsData(request, obj):
	titles = []
	times = []

	Running_Times = RunTime.objects.filter(user=request.user)

	for entry in Running_Times:
		titles.append(entry.title)
		times.append(entry.run_time)
	json_titles = json.dumps(titles)
	context={'titles':json_titles, 'times':times}
	return render(request, "main/results_data.html", context)

def delete_time(request, pk):
	Running_Time = RunTime.objects.get(id=pk)
	Running_Time.delete()
	return HttpResponseRedirect('/my_results'+'/'+request.user.username)

@login_required(login_url='/login')
def profile(request):
	users = User.objects.all()
	current_user = request.user


	context = {'users':users, 'current_user': current_user}

	return render(request, "main/profile.html", context)

def edit_time(request, pk):
	Running_Time = RunTime.objects.get(id=pk)
	form = TimeForm(instance=Running_Time)
	current_user=request.user

	if request.method == 'POST':
		form = TimeForm(request.POST, instance=Running_Time)
		if form.is_valid():
			cd = form.cleaned_data
			if cd['user'] == request.user:
				form.save()
				return redirect('/my_results/'+current_user.username)
			else:
				return redirect('/cheeky')


	context = {'form':form}

	return render(request, 'main/edit.html', context)

def change_details(request, key):
	current_user = request.user
	#current_user = User.objects.get(username=request.user.username)
	form = RegisterForm(instance = current_user)
	
	if request.method == 'POST':
		form = RegisterForm(request.POST, instance=current_user)
		if form.is_valid():
			form.save()
			return redirect('/profile')

	context = {'form':form}

	return render(request, 'main/edit_profile.html', context)

@login_required(login_url='/login')
def nick_name(request):
	nicknames = nickname.objects.all()
	form = nicknameForm(initial={'user':request.user})
	if request.method == 'POST':
		form = nicknameForm(request.POST, initial={'user':request.user})
		if form.is_valid():
			form.save()
			return redirect('/nickname/')
	else:
		form = nicknameForm(initial={'user':request.user})

	context = {'form':form, 'nicknames':nicknames}

	return render(request, 'main/nickname.html', context)


def SeeResults(request, pk):
	users = User.objects.all()
	for user in users:
		if user.last_name == pk:
			my_user = user

	user_results = RunTime.objects.filter(user = my_user).order_by('date')
	the_results = []
	the_times = []
	my_labels = []
	for entry in user_results:
		the_results.append([entry.date, entry.run_time])
		the_times.append(entry.run_time)
		my_labels.append(entry.title)

	the_results.reverse()

	json_titles = json.dumps(my_labels)

	context = {'results':the_results, 'the_user':my_user, 
	'titles':json_titles, 'RunTimes': the_times}

	return render(request, 'main/see_results.html', context)



