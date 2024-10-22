from django.db import models
from django.contrib.auth import get_user_model
from .constants import STATUS_CHOICES,SPLIT_CHOICES

User = get_user_model()

# To handle a Expense
class Expense(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_by = models.ForeignKey(User, related_name='expenses', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    split_method = models.CharField(max_length=25, choices=SPLIT_CHOICES.choices,default=SPLIT_CHOICES.EQUAL)

    def __str__(self):
        return f"{self.description} - {self.amount} by {self.paid_by.username}"


# Split class will handle the splits between users for a particular Expense . There can be multiple split instances for a single Expense Instance.
class ExpenseSplit(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='splits')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='splits')
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES.choices, default=STATUS_CHOICES.PENDING)

    def update_payment(self, payment_amount):
        self.amount_paid += payment_amount
        self.amount_due -= payment_amount
        if self.amount_due <= 0:
            self.status =  STATUS_CHOICES.COMPLETED
        elif self.amount_paid > 0:
            self.status = STATUS_CHOICES.PARTIALLY_PAID
        self.save()
