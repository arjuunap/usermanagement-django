from django.urls import path
from . import views
app_name  = 'adminpanel'
urlpatterns = [
    path("",views.admin_panel,name='admin-panel'),
    path('logout/',views.admin_logout,name='logout'),
    path('login/',views.admin_login,name='login'),
    path("edit-user/<int:id>/", views.edit_user, name="edit-user"),
]