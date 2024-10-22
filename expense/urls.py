from django.urls import path
from .views import AddExpenseView,UserExpensesView,OverallExpensesView,BalanceSheetView,UserPayExpensesView

urlpatterns = [
    path('add', AddExpenseView.as_view(), name='add-expense'),
    path('user-expenses', UserExpensesView.as_view(), name='user-expenses'),
    path('user-pay-expense/<int:expense_id>', UserPayExpensesView.as_view(), name='pay-expense'),
    path('overall-expenses', OverallExpensesView.as_view(), name='overall-expenses'),
    path('balance-sheet/download/', BalanceSheetView.as_view(), name='download-balance-sheet'),
]
