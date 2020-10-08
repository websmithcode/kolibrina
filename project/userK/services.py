import datetime
from django.conf import settings

from userK.models import User as User
from . import forms
from .phone_validate import phone_validate
from media import forms as media_forms, services as media_services


def write_user_model(username, values):
    user_model = get_user_model(username=username)
    fields = []
    for value in values:
        fields.append(value)
        if value != 'hideMyName' and value != 'phoneNumber':
            user_model.__dict__[value] = values[value]
        elif value == 'phoneNumber':
            result = phone_validate(values['phoneNumber'])
            if result['status'] == 'OK':
                user_model.__dict__[value] = result['phone']
            elif result['status'] == 'error':
                return result

    if 'hideMyName' in fields:
        user_model.__dict__['hideMyName'] = True
    else:
        user_model.__dict__['hideMyName'] = False

    user_model.save()
    return {'status': 'OK'}


def create_render_data(request, ):
    userModel = get_user_model(request.user)
    maxDateField = '-'.join((str(datetime.date.today().year), datetime.date.today().strftime('%m-%d')))
    minDateField = '-'.join((str(datetime.date.today().year - 100), datetime.date.today().strftime('%m-%d')))

    team_players_list = _get_teammates(request.user)

    data = {'userID': f'{request.user.id}'.rjust(7, '0'),
            'gender': userModel.gender,
            'form': _get_form_values(userModel=userModel),
            'errors': [],
            'error_phone': '',
            'level': get_user_rating_lvl_dif(userModel.rating),
            'AvatarForm': media_forms.AvatarForm(initial={'user': request.user}),
            'AvatarImage': media_services.get_avatar(user=request.user),
            'mainBanner': media_services.get_banner(),
            'league': str(request.user.league),
            'maxDateField': maxDateField,
            'minDateField': minDateField,
            'users_list': _get_users_and_id_list(request.user),
            'team': _get_team_name_or_blank(request.user),
            'team_players_list': team_players_list,
            'new_teammate_num': len(team_players_list)+1,
            'team_number': settings.TEAM_NUMBERS,
            'invite_teams_list': _get_invite_teams_list(request.user)}
    return data


def get_user_rating_lvl_dif(rating):
    rating = round(float(rating), 3)

    def r(rating, max, deltamax, level):
        for i in range(0, 981):
            if rating < max:
                return {'rating': str(rating) + '/' + str(max), 'numLevel': i, 'level': level}
            else:
                max += deltamax

    if rating < 1000:
        max = 100
        deltamax = 100
        level = 'J (юниор)'
        return r(rating, max, deltamax, level)
    elif rating < 3000:
        max = 1000
        deltamax = 200
        level = 'L (любитель)'
        return r(rating, max, deltamax, level)
    elif rating < 6000:
        max = 3000
        deltamax = 300
        level = 'Z (знаток)'
        return r(rating, max, deltamax, level)
    elif rating < 10000:
        max = 6000
        deltamax = 400
        level = 'M (мастер)'
        return r(rating, max, deltamax, level)
    else:
        max = 10000
        deltamax = 500
        level = 'P (профи)'
        return r(rating, max, deltamax, level)


def get_user_model(username):
    return User.objects.get(username=username)


def _get_users_and_id_list(current_user):
    users_list = User.objects.filter(is_active=1)
    users_and_id_list = []
    for user in users_list:
        if user.username != current_user.username:
            user_id = str(user.id).rjust(7, '0')
            user_username = user.username
            users_and_id_list.append(f'{user_username} | {user_id}')
    return users_and_id_list


def _get_form_values(userModel):
    userModel = userModel.__dict__
    try:
        form = forms.EditUser(initial={
            'birthday': userModel['birthday'].__format__('%Y-%m-%d'),
            'gender': userModel['gender'],
            'country': userModel['country'],
            'area': userModel['area'],
            'city': userModel['city'],
        })
    except TypeError:
        form = forms.EditUser(initial={
            'birthday': '',
            'gender': userModel['gender'],
            'country': userModel['country'],
            'area': userModel['area'],
            'city': userModel['city'],
        })
    return form


def _get_team_name_or_blank(user):
    if user.team:
        return user.team
    else:
        return ''


def _get_invite_teams_list(user):
    invite_list = user.invitetoteam_set.all()
    return invite_list


def _get_teammates(user):
    if user.team:
        return user.team.user_set.all()
    else:
        return ''
