from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Paid  # Import the Paid model from your app's models

@receiver(post_save, sender=Paid)
def update_loan_amount_paid(sender, instance, **kwargs):
    instance.loan.update_amount_paid()
