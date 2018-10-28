from django.urls import path, re_path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ListView, CreateView, EditView

urlpatterns = {
    re_path(r'^auth/', include('rest_framework.urls',
                             namespace='rest_framework')),
    re_path(r'^listitems/$', ListView.as_view(), name='listitems' ),
    re_path(r'^createitem/$', CreateView.as_view(), name='createitem'),
    re_path(r'^edit/(?P<pk>[0-9]+)/$', EditView.as_view(), name='edit')
}

urlpatterns = format_suffix_patterns(urlpatterns)