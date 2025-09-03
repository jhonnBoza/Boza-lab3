from django.urls import path
from . import views

urlpatterns = [
    path('', views.exam_list, name='exam_list'),
    path('exam/<int:exam_id>/', views.exam_detail, name='exam_detail'),
    path('exam/create/', views.exam_create, name='exam_create'),
    path('exam/<int:exam_id>/question/add/', views.question_create, name='question_create'),
    #Nuevas rutas para tomar exámenes y ver resultados
    path('exam/<int:exam_id>/take/', views.take_exam, name='take_exam'),
    path('result/<int:attempt_id>/', views.exam_result, name='exam_result'),
]
