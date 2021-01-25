from django.shortcuts import render, redirect
from django.views.generic import FormView
from .forms import NewPlanForm
from api.discord_api import get_guild_info, get_user_info
from DiscordPlanner.constants import *
from pymongo import MongoClient
from django.utils.dateparse import parse_datetime
import datetime

# Create your views here.


def plans(request):
    cluster = MongoClient(MONGO_URL)
    db = cluster["DiscordPlannerDB"]
    collection = db["Plans"]
    guilds = get_guild_info(request.COOKIES.get(
        'token_type'), request.COOKIES.get('access_token'))
    user_info = get_user_info(request.COOKIES.get(
        'token_type'), request.COOKIES.get('access_token'))
    guild_ids = [int(g['id']) for g in guilds]
    guild_names = {int(g['id']): g['name'] for g in guilds}
    now = datetime.datetime.now()
    query = {'guild': {'$in': guild_ids}, 'time': {"$gte": now}}
    plans = list(collection.find(query))
    print(plans)
    for p in plans:
        p['guild'] = guild_names[p['guild']]
    context = {"plans": plans}

    return render(request, 'plans.html', context)


def newPlan(request):
    if not request.COOKIES.get('access_token'):
        return redirect('/login')
    if request.method == 'POST':
        cluster = MongoClient(MONGO_URL)
        db = cluster["DiscordPlannerDB"]
        collection = db["Plans"]
        user_info = get_user_info(request.COOKIES.get(
            'token_type'), request.COOKIES.get('access_token'))
        guild = int(request.POST['guild'])
        plan_name = request.POST['plan_name']
        time = parse_datetime(request.POST['datetime'])
        print(time)

        plan_info = {'guild': guild,
                     'name': plan_name,
                     'time': time,
                     'attendee': [user_info['id']]}

        if request.POST['attendee_num']:
            plan_info['max_attendee'] = int(request.POST['attendee_num'])
        print(plan_info)
        collection.insert_one(plan_info)
        return redirect('/plans')

    else:
        guilds = get_guild_info(request.COOKIES.get(
            'token_type'), request.COOKIES.get('access_token'))
        guild_list = []
        for guild in guilds:
            guild_list.append((guild['id'], guild['name']))
        my_form = NewPlanForm()
        my_form.fields['guild'].choices = guild_list
        context = {
            'form': my_form,
        }
        return render(request, 'new_plan.html', context)
