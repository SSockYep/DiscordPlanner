from django.shortcuts import render, redirect
from django.views.generic import FormView
from .forms import NewPlanForm
from baseApp.discord_api import get_guild_info, get_user_info
from DiscordPlanner.constants import *
from pymongo import MongoClient
from django.utils.dateparse import parse_datetime
import datetime


def planView(request):
    if not request.COOKIES.get('access_token'):
        return redirect('/login')
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


def attendPlanView(request):
    if not request.COOKIES.get('access_token'):
        return redirect('/login')


def newPlanView(request):
    if not request.COOKIES.get('access_token'):
        return redirect('/login')
    guilds = get_guild_info(request.COOKIES.get(
        'token_type'), request.COOKIES.get('access_token'))
    guild_list = []
    for guild in guilds:
        guild_list.append((int(guild['id']), guild['name']))
    if request.method == 'POST':
        user_info = get_user_info(request.COOKIES.get(
            'token_type'), request.COOKIES.get('access_token'))

        plan_form = NewPlanForm(request.POST)
        plan_form.fields['guild'].choices = guild_list
        if plan_form.is_valid():
            print('asdf')
            plan = plan_form.save()
            return redirect('/plans')
        else:
            return redirect('/plans/new')

    else:
        plan_form = NewPlanForm()
        plan_form.fields['guild'].choices = guild_list
        context = {
            'form': plan_form,
        }
        return render(request, 'new_plan.html', context)
