from django.urls import path
from .views import index, by_rubric, BbCreateView, test_cookies, test_session, test_1, test_2

urlpatterns = [
    path('add/', BbCreateView.as_view(), name='add'),
    path('<int:rubric_id>/', by_rubric, name="by_rubric"),
    path('', index, name="index"),
    path('test/', test_cookies),
    path('test_session/', test_session),
    path('test_1/', test_1),
    path('test_2/', test_2),
]
