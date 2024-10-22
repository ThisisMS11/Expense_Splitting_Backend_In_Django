from django.db import models

class STATUS_CHOICES(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    PARTIALLY_PAID = 'PARTIALLY_PAID', 'Partially Paid'
    COMPLETED = 'COMPLETED', 'Completed'

class SPLIT_CHOICES(models.TextChoices):
    EQUAL = 'EQUAL', 'Equal'
    EXACT = 'EXACT', 'Exact'
    PERCENTAGE = 'PERCENTAGE', 'Percentage'
