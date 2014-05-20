from django.views.generic.simple import direct_to_template
from django.http import HttpResponseRedirect

import datetime

from google.appengine.api import users

from diary.models import Diary

def login_page(request):
    if users.get_current_user():
        # has logged in
        return diary_page(request, users.get_current_user().nickname())
    else:
        # has logged out
        return HttpResponseRedirect(users.create_login_url('/'))


def diary_page(request, diary_owner):
    if request.method == 'POST':
        diary_key = Diary.get_key_from_name(diary_owner)
        # get DB
        diary = Diary(parent=diary_key)
        # set author
        diary.author = diary_owner[0:diary_owner.find('@')]
        # set weahter
        diary.weather = "Don't remember"
        weather = request.POST.get('weather')
        if weather:
            diary.weather = weather
        # set content
        diary.content = request.POST.get('content')
        # set date
        diary.date = request.POST.get('diary_date')
        # put to DB
        diary.put()
        
        return HttpResponseRedirect('/')

    # get key
    diary_key = Diary.get_key_from_name(diary_owner)
    # make query for select data ordered dsec
    diary_query = Diary.all().ancestor(diary_key).order('-date')
    # get result set
    diaries = diary_query.fetch(2)
    
    # get user, if exist current user
    if users.get_current_user():
        # create logout url
        url = users.create_logout_url('/')
        url_linktext = 'Logout'
    else:
        # create login url
        return HttpResponseRedirect(users.create_login_url('/'))
        
    # set up values for use in template
    template_values = {
        'diaries': diaries,
        'diary_author': diary_owner[0:diary_owner.find('@')],
        'diary_owner': diary_owner,
        'url': url,
        'url_linktext': url_linktext,
    }
    
    return direct_to_template(request, 'diary/diary_page.html', template_values)


def diary_writer(request):
    if request.method == 'POST':
        # get user, if exist current user
        if users.get_current_user():
            # create logout url
            url = users.create_login_url('/')
            url_linktext = 'Logout'
        else:
            # create login url
            return HttpResponseRedirect(users.create_login_url('/'))
            
        # set up values for use in template
        diarwy_owner = request.POST.get('diary_owner');
        template_values = {
            'diary_date': datetime.datetime.now().strftime('%Y. %m. %d.'),
            'diary_author': diarwy_owner[0:diarwy_owner.find('@')],
            'diary_owner': diarwy_owner,
            'url': url,
            'url_linktext': url_linktext,
        }
        
        return direct_to_template(request, 'diary/post_page.html', template_values)
     
    return HttpResponseRedirect('/')
