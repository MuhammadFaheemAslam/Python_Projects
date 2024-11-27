from django.urls import path
from . import views

urlpatterns = [
	path('',views.index, name='index'),
    path('add/', views.addTodo, name='addTodo'),
    path('complete/<todo_id>', views.completeTodo, name='complete'),
    path('search/', views.search_todo, name='search'),
    path('uncomplete/<todo_id>', views.uncompleteTodo, name='uncomplete'),
    path('deletecompleted', views.deletecompleted, name='deletecompleted'),
    path('deleteall', views.deleteall, name='deleteall')
    ]
