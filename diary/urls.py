from django.conf.urls.defaults import *
from diary.views import login_page, diary_writer

# redirect url
urlpatterns = patterns('',
    (r'^writer/$', diary_writer),
    (r'^$', login_page),
)