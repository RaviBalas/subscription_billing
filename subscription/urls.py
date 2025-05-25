from django.urls import path

from .views import SubscribePlanView, UnSubscribePlanView, PlanView

urlpatterns = [
    path("plans/", PlanView.as_view()),
    path("subscribe/", SubscribePlanView.as_view()),
    path("unsubscribe/", UnSubscribePlanView.as_view()),
]
