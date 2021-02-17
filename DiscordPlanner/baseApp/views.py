from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .discord_api import exchange_code, get_guild_info, get_user_info
from .models import User
from DiscordPlanner.constants import *


def mainView(request):
    if request.COOKIES.get('access_token'):
        context = {'token': True}
    else:
        context = {'token': False}
    context['invite_url'] = BOT_INVITE
    return render(request, 'main.html', context)


def testView(request):
    try:
        code = request.GET['code']
        print('code:', code)
        r = exchange_code(code)
        print('r:', r)
        guilds = get_guild_info(r['token_type'], r['access_token'])
        print(guilds)
        response = HttpResponse(str(r))
        response.set_cookie(key='token_type', value=r['token_type'])
        response.set_cookie(key='access_token', value=r['access_token'])
    except:
        return HttpResponse('no code')
    return response


def loginView(request):
    if request.COOKIES.get('access_token'):
        return redirect('/')
    elif request.GET.get('code'):
        code = request.GET['code']
        r = exchange_code(
            code, 'http://127.0.0.1:8000/login')
        user_info = get_user_info(r['token_type'], r['access_token'])
        try:
            User.objects.get(uid=int(user_info['id']))
        except ObjectDoesNotExist:
            new_user = User(
                uid=int(user_info['id']), name=user_info['username'])
            new_user.save()
        response = redirect('/')
        response.set_cookie(key='token_type', value=r['token_type'])
        response.set_cookie(key='access_token', value=r['access_token'])
        return response
    else:
        return redirect('https://discord.com/api/oauth2/authorize?client_id=781130078272094209&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Flogin&response_type=code&scope=identify%20guilds')
