from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import ExpenseSerializer

# Endpoint to add an expense
class AddExpenseView(generics.CreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(paid_by=self.request.user)


