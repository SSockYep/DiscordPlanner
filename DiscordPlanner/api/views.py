from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from plans.models import Plan
from django.http import HttpResponse, JsonResponse
from baseApp.models import User, Guild
from baseApp.discord_api import get_user_info, get_guild_info
import json


class APIBaseView(View):
    @staticmethod
    def response(data={}, message='', status=200):
        result = {
            'data': data,
            'message': message,
        }
        return JsonResponse(result, status=status)


class CreateGuildView(APIBaseView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateGuildView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            gid = request.POST.get('gid', '')
            name = request.POST.get('name', '')
        except:
            return self.response(message='error', status=400)

        guild, created = Guild.objects.get_or_create(name=name, gid=gid)
        if created:
            guild.save()

        return self.response({'gid': guild.gid, 'name': guild.name}, 'guild created')


class CreateUserView(APIBaseView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(GuildRegisterView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            uid = request.POST.get('uid', '')
            name = request.POST.get('name', '')
        except:
            return self.response(message='error', status=400)

        user = User(uid=uid, name=name)
        user.save()

        return self.response({'uid': user.uid, 'name': user.name}, 'user greated')


class CreateUserAndJoinGuildView(APIBaseView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CreateUserAndJoinGuildView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        try:
            uid = request.POST.get('uid', '')
            name = request.POST.get('name', '')
            gid = request.POST.get('gid', '')
        except:
            return self.response(message='error', status=400)

        user, created = User.objects.get_or_create(uid=uid, name=name)
        if created:
            user.save()

        guild = Guild.objects.get(gid=gid)
        guild.user.add(user)
        guild.save()

        return self.response({'uid': user.uid, 'name': user.name, 'guild_name': guild.name}, 'user created and joined')


class JoinGuildView(APIBaseView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(JoinGuildView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        print(request)
        try:
            gid = request.POST.get('gid', '')
            uid = request.POST.get('uid', '')
            guild = Guild.objects.get(gid=gid)
            user = User.objects.get(uid=uid)
        except:
            return self.response(message='error', status=400)

        guild.user.add(user)
        guild.save()

        return self.response({'gid': guild.gid, 'guild_name': guild.name, 'user': user.name},
                             '%s registered to %s' % (user.name, guild.name))


class GetUsersView(APIBaseView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(GetUsersView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        try:
            gid = request.GET.get('gid', '')
        except:
            return self.response(message='no gid', status=400)
        try:
            guild = Guild.objects.get(gid=gid)
        except:
            return self.response(message='no guild with gid %s' % gid, status=400)
        users = guild.user.all()
        response_data = {"users": list(users)}
        return self.response(response_data, 'user list of guild %s' % guild.name)


class GetAllGuildsView(APIBaseView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(GetAllGuildsView).dispatch(request, *args, **kwargs)

    def get(self, request):
        guilds = Guild.objects.all()
        response_data = {"guilds": list(guilds)}
        return self.response(response_data, 'guild list' % guild.name)
