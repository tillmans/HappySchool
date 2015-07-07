from django.conf.urls import url,patterns
from django.views.generic import TemplateView
from photo import settings

urlpatterns = patterns('Fun.views',
    url(r'^$','index',name='index'),

    url(r'^provinces/$','province_list',name = 'province_list'),
    url(r'^cities/$','city_list',name = 'city_list'),
    url(r'^districts/$','district_list',name = 'district_list'),

    url(r'^registerSchoolAdministrator/$','registerSchoolAdministator',name = 'registerSchoolAdministator'),
    url(r'^createSchool/$','createSchool',name = 'createSchool'),
    url(r'^registerTeacher/$','registerTeacher',name = 'registerTeacher'),
    url(r'^registerParent/$','registerParent',name = 'registerParent'),

)
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$',"django.views.static.serve",{"document_root": settings.MEDIA_ROOT,}),
