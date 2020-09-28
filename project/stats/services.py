def get_sym_plus_if_num_is_positive(num):
    sym = ''
    if num > 0:
        sym = '+'
    return sym


def get_sum_score_user(user, date_range=False):
    if not date_range:
        score_history = list(user.scorehistory_set.values('score'))
    else:
        score_history = list(user.scorehistory_set.filter(date__range=date_range).values('score'))

    def _get_sum(scores):
        scores_list = []
        for i in scores:
            scores_list.append(i['score'])
        return sum(scores_list)

    return _get_sum(score_history)


def init_league(user):
    league = user.league
    rating = user.rating
    threshold = _get_lower_threshold(rating=rating, league=league)
    if threshold['status'] == 'SWITCH':
        user.league = threshold['new_league']


def _get_lower_threshold(rating, league):
    if 1000 <= rating < 3000 and (league in ['l1', 'l2']):
        return {'status': 'SWITCH', 'new_league': 'l3'}
    elif 3000 <= rating < 6000 and (league in ['l1', 'l2', 'l3']):
        return {'status': 'SWITCH', 'new_league': 'l4'}
    elif 6000 <= rating < 10000 and (league in ['l1', 'l2', 'l3', 'l4']):
        return {'status': 'SWITCH', 'new_league': 'l5'}
    elif rating >= 10000 and (league in ['l1', 'l2', 'l3', 'l5']):
        return {'status': 'SWITCH', 'new_league': 'l6'}
    else:
        return {'status': 'OK'}