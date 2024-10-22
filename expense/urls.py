from django.urls import path
from .views import AddExpenseView

urlpatterns = [
    path('add', AddExpenseView.as_view(), name='add-expense'),
]
