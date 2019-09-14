from django.urls import path
from django.conf import settings

from . import views

app_name = 'polls'
urlpatterns = [
    path('create/ajax_calls/search/', views.autocompleteModel),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('create/', views.CreateQuestionView.as_view(), name='create')
]
