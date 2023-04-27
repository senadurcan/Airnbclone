
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index , name='anasayfa'),
    path('detay/',detay, name='detay'),
    path('profil/',profil, name='profil'),
    path('hesap/',hesap, name='hesap'),
    path('host/' , host , name="host"),
    path('kisisel/',hesapKisisel,name='kisisel'),
    path('guvenlik/',guvenlik,name='guvenlik'),
    path('odeme/',payment,name='odeme'),
    path('vergiler/',vergiler,name='vergiler'),
    path('bildirim/',bildirim,name='bildirim'),
    path('gizlilik/',gizlilik,name='gizlilik'),
    path('tercihler/',tercihler,name='tercihler'),
    path('seyehat/',seyehat,name='seyehat'),
    path('sahiplik/',sahiplik,name='sahiplik'),
    path('misafir/',misafir,name='misafir'),
    path('postForm/',postForm,name='postForm'),
    path('LoginRegister/' , loginregister , name="loginregister"),
    path('logout/' , logout_request , name="logout")
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
