from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Paid, Loan  # Import the Paid and Loan models from your app's models

@receiver(post_save, sender=Paid)
def update_loan_amount_paid(sender, instance, **kwargs):
    # Get the original amount_paid from the Loan model
    original_amount_paid = instance.loan.amount_paid

    # Get the new amount from the Paid model
    new_amount = instance.amount

    # Calculate the updated amount_paid by adding the original and new amounts
    updated_amount_paid = original_amount_paid + new_amount

    # Update the Loan model with the new amount_paid
    instance.loan.amount_paid = updated_amount_paid
    instance.loan.save()
