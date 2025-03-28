
from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signup),
    path('signup/', views.signup),  
    path('login/', views.login),
    path('todopage/', views.todo),
    path('edit_todo/<int:srno>', views.edit_todo, name = 'edit_todo'),
    path('delete_todo/<int:srno>', views.delete_todo),
    path('signout/', views.signout, name = 'signout')
]
