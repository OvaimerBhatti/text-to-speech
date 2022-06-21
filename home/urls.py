from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from home import views
from home.auth import auth_middleware


urlpatterns = [
    path('',views.login_url,name="home"),
    path('login',views.login_url,name="login"),
    path('signup',views.signup_url,name="signup"),
    path('logout',views.logout_url,name="logout"),
    path('converter',auth_middleware(views.converter_url),name="converter")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)