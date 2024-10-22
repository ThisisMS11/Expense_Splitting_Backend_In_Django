from django.urls import path
from .views import AddExpenseView,UserExpensesView,OverallExpensesView

urlpatterns = [
    path('add', AddExpenseView.as_view(), name='add-expense'),
    path('user-expenses', UserExpensesView.as_view(), name='user-expenses'),
    path('overall-expenses', OverallExpensesView.as_view(), name='overall-expenses'),

]
