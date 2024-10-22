from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import ExpenseSerializer
from .models import Expense
from django.db import models
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from django.db.models import Sum, Q

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


class BalanceSheetView(APIView):
    permission_classes = [IsAuthenticated]

    def get_individual_expenses(self, user):
        # Fetch individual expenses where the user paid or is part of the split
        return Expense.objects.filter(
            Q(paid_by=user) | Q(splits__user=user)
        ).distinct()

    def get_overall_expenses(self):
        # Fetch all expenses
        return Expense.objects.all()

    def generate_pdf(self, expenses, individual_expenses, response):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        pdf.drawString(100, 800, "Balance Sheet Report")

        # Writing individual expenses
        pdf.drawString(100, 780, "Individual Expenses")
        y = 760
        for expense in individual_expenses:
            pdf.drawString(100, y, f"Description: {expense.description}, Amount: {expense.amount}, Paid By: {expense.paid_by.username}")
            y -= 20
            for split in expense.splits.filter(user=self.request.user):
                pdf.drawString(120, y, f"User: {split.user.username}, Amount Due: {split.amount_due}, Amount Paid: {split.amount_paid}, Status: {split.status}")
                y -= 20

        # Writing overall expenses
        pdf.drawString(100, y - 40, "Overall Expenses")
        y -= 60
        for expense in expenses:
            pdf.drawString(100, y, f"Description: {expense.description}, Amount: {expense.amount}, Paid By: {expense.paid_by.username}")
            y -= 20
            for split in expense.splits.all():
                pdf.drawString(120, y, f"User: {split.user.username}, Amount Due: {split.amount_due}, Amount Paid: {split.amount_paid}, Status: {split.status}")
                y -= 20

        pdf.showPage()
        pdf.save()
        pdf_content = buffer.getvalue()
        buffer.close()

        response.write(pdf_content)

    def get(self, request, format=None):
        # Fetch all the expenses and individual expenses for the user
        individual_expenses = self.get_individual_expenses(request.user)
        overall_expenses = self.get_overall_expenses()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="balance_sheet.pdf"'
        self.generate_pdf(overall_expenses, individual_expenses, response)

        return response