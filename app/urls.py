from django.conf import settings
from django.urls import path
from app import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('ask/', views.ask, name='ask'),
    path('hot/', views.hot, name='hot'),
    path('logout/', views.logout, name='logout'),
    path('tag/<str:tag>/', views.tag_id, name='tag'),
    path('question/<int:question_id>/', views.single_question, name='question'),
    path('settings/', views.settings, name='settings'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)