from rest_framework import serializers
from .models import Expense, ExpenseSplit
from django.contrib.auth import get_user_model
from .constants import SPLIT_CHOICES,STATUS_CHOICES

User = get_user_model()

class SplitSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField() 
    amount_due = serializers.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = serializers.ChoiceField(choices=STATUS_CHOICES.choices, read_only=True)

    class Meta:
        model = ExpenseSplit
        fields = ['user', 'amount_due', 'amount_paid', 'status']

    def validate(self, data):
        if data['amount_paid'] > data['amount_due']:
            raise serializers.ValidationError("Amount paid cannot be more than the amount due.")
        return data

    def update(self, instance, validated_data):
        payment_amount = validated_data.get('amount_paid', instance.amount_paid)
        instance.update_payment(payment_amount)
        return instance


class ExpenseSerializer(serializers.ModelSerializer):
    splits = SplitSerializer(many=True, read_only=True)
    participants = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )
    split_method = serializers.ChoiceField(choices=SPLIT_CHOICES.choices)
    exact_amounts = serializers.DictField(child=serializers.DecimalField(max_digits=10, decimal_places=2), required=False)
    percentages = serializers.DictField(child=serializers.DecimalField(max_digits=5, decimal_places=2), required=False)
    
    # Make paid_by read-only since it will be set in create()
    paid_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'description', 'amount', 'paid_by', 'split_method', 'participants', 'exact_amounts', 'percentages', 'splits']

    def validate(self, data):
        if data['split_method'] == SPLIT_CHOICES.EXACT and not data.get('exact_amounts'):
            raise serializers.ValidationError("Exact amounts required for exact split.")
        if data['split_method'] == SPLIT_CHOICES.PERCENTAGE and not data.get('percentages'):
            raise serializers.ValidationError("Percentages required for percentage split.")
        if data['split_method'] == SPLIT_CHOICES.PERCENTAGE and sum(data['percentages'].values()) != 100:
            raise serializers.ValidationError("Percentages must add up to 100.")
        return data

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        split_method = validated_data.pop('split_method')
        exact_amounts = validated_data.pop('exact_amounts', {})
        percentages = validated_data.pop('percentages', {})

        # Create the expense with the paid_by field
        expense = Expense.objects.create(**validated_data)

        users = User.objects.filter(id__in=participants)

        # Calculate splits based on method
        if split_method == SPLIT_CHOICES.EQUAL:
            share = expense.amount / len(users)
            for user in users:
                if user == expense.paid_by:
                    # The user who paid the expense, mark their status as COMPLETED
                    ExpenseSplit.objects.create(expense=expense, user=user, amount_due=0, amount_paid=share, status=STATUS_CHOICES.COMPLETED)
                else:
                    ExpenseSplit.objects.create(expense=expense, user=user, amount_due=share)

        elif split_method == SPLIT_CHOICES.EXACT:
            for user_id, amount in exact_amounts.items():
                user = User.objects.get(id=user_id)
                if user ==  expense.paid_by:
                    # The user who paid the expense, mark their status as COMPLETED
                    ExpenseSplit.objects.create(expense=expense, user=user, amount_due=0, amount_paid=amount, status=STATUS_CHOICES.COMPLETED)
                else:
                    ExpenseSplit.objects.create(expense=expense, user=user, amount_due=amount)

        elif split_method == SPLIT_CHOICES.PERCENTAGE:
            for user_id, percentage in percentages.items():
                user = User.objects.get(id=user_id)
                amount_due = (percentage / 100) * expense.amount
                if user ==  expense.paid_by:
                    # The user who paid the expense, mark their status as COMPLETED
                    ExpenseSplit.objects.create(expense=expense, user=user, amount_due=0, amount_paid=amount_due, status=STATUS_CHOICES.COMPLETED)
                else:
                    ExpenseSplit.objects.create(expense=expense, user=user, amount_due=amount_due)

        return expense

