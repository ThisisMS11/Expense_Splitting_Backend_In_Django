from django.contrib import admin
from .models import Expense,ExpenseSplit
# Register your models here.

admin.site.register(Expense)
admin.site.register(ExpenseSplit)
