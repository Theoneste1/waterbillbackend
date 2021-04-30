from django.urls import path
from .views import Login, CreateAccount, CalculateBillView, DashboardView

urlpatterns = [
    path('login/', Login.as_view()),
    path('register/', CreateAccount.as_view()),
    path('make-bill/<str:token>', CalculateBillView.as_view()),
    path('dashboard/<str:token>', DashboardView.as_view())
]