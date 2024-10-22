from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import ExpenseSerializer
from .models import Expense
from django.db import models

# Endpoint to add an expense
class AddExpenseView(generics.CreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(paid_by=self.request.user)

# Endpoint to retrieve individual user's expenses
class UserExpensesView(generics.ListAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter expenses where the user is either the one who paid or a participant in splits
        return Expense.objects.filter(
            models.Q(paid_by=self.request.user) | models.Q(splits__user=self.request.user)
        ).distinct()

# Endpoint to retrieve all expenses (overall expenses)
class OverallExpensesView(generics.ListAPIView):
    queryset = Expense.objects.all()  # Fetch all expenses
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated] 