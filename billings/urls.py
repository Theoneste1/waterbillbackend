from django.urls import path
from .views import Login, CreateAccount, CalculateBillView, DashboardView

urlpatterns = [
    path('logins/', Login.as_view()),
    path('registers/', CreateAccount.as_view()),
    path('make-bills/<str:token>', CalculateBillView.as_view()),
    path('dashboards/<str:token>', DashboardView.as_view())
]