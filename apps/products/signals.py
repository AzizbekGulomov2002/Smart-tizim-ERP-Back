from django.db.models.signals import post_delete
from django.dispatch import receiver
from apps.finance.models import FinanceOutcome
from apps.products.models import StorageProduct


@receiver(post_delete, sender=StorageProduct)
def delete_related_finance_outcome(sender, instance, **kwargs):
    FinanceOutcome.objects.filter(
        user=instance.user,
        supplier=instance.supplier,
        tranzaction_type__transaction_type='ombor',
        tranzaction_type__action_type='chiqim'
    ).delete()