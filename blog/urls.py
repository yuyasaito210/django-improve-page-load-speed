from django.urls import path
from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='posts'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name = 'post-detail'),
]