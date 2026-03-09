from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.login_view,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout_view,name='logout')
]
