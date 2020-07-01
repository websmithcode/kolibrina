from django.shortcuts import render, redirect
from . import forms, level
from .phone_isValid import phone_isValid
from userK.models import CustomUser as User
from media import forms as media
from django.conf import settings
import os


# class account(FormView):
#     form_class = forms.EditUser
#     success_url = "/account/"
#     template_name = "userK/account.html"

# def account(request):
#     return HttpResponse('{{ forms.EditUser.as_p }}')


def account(request):
    if request.user.is_authenticated:
        uDir = [str(settings.MEDIA_ROOT).replace('\\', '/'), 'user_' + str(request.user)]
        if os.listdir(uDir[0]).__contains__(uDir[1]):
            uDir += 'user_' + str(request.user)
            ava = '/' + uDir[0].split('/')[-3] + '/' + uDir[0].split('/')[-2] + '/' + uDir[1] + '/' + \
                  os.listdir(uDir[0] + uDir[1])[0]
        else:
            ava = False
        u = User.objects.get(id=request.user.id).__dict__
        try:
            form = forms.EditUser(initial={
                'birthday': u['birthday'].__format__('%Y-%m-%d'), 'gender': u['gender'], 'country': u['country'],
                'area': u['area'], 'city': u['city'],
            })
        except TypeError:
            form = forms.EditUser(initial={
                'birthday': '', 'gender': u['gender'], 'country': u['country'],
                'area': u['area'], 'city': u['city'],
            })
        data = {'userID': str(request.user.id).rjust(7, '0'), 'gender': u['gender'],
                'form': form, 'errors': [], 'error_phone': '', 'r': request.user,
                'level': level.op(int(u['opLVL'])), 'AvatarForm': media.AvatarForm(initial={'user': request.user, }),
                'AvatarImage': ava,
                }
        if request.POST:
            if request._post.__contains__('phoneNumber'):
                phone = request._post['phoneNumber']
            else:
                phone = u['phoneNumber']
            phone, data['errors'], data['error_phone'] = phone_isValid(phone, User, data)
            if data['errors']:
                return render(request, 'userK/account.html', data)
            for n, i in enumerate(request._post):
                if i == 'birthday':
                    u['birthday'] = request._post[i]
                if n > 0 and n != 3 and i != 'phoneNumber':
                    u[i] = request._post[i]
                elif n == 3:
                    if i != 'hideMyName':
                        u['hideMyName'] = False
                    else:
                        u['hideMyName'] = True
                elif i == 'phoneNumber':
                    u['phoneNumber'] = '8' + ''.join(phone)
            us = User.objects.get(id=request.user.id)
            us.__dict__ = u
            us.save()
            return redirect('account')
        else:
            return render(request, 'userK/account.html', data)
    else:
        return redirect('login')
