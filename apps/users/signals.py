from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from apps.users.models import Company, CompanyPayments, User


@receiver(post_save, sender=Company)
def update_workers_is_active(sender, instance, **kwargs):
    users = User.objects.filter(company_id=instance.id)
    users.update(is_active=instance.is_active)

@receiver(post_delete, sender=Company)
def delete_related_users(sender, instance, **kwargs):
    users = User.objects.filter(company_id=instance.id)
    users.delete()


@receiver(post_save, sender=CompanyPayments)
@receiver(post_delete, sender=CompanyPayments)
def check_company_payment_status(sender, instance, **kwargs):
    company_id = instance.company_id
    today = timezone.now().date()
    overdue_payments = CompanyPayments.objects.filter(company_id=company_id, finish__lte=today).exists()
    
    company = Company.objects.get(id=company_id)
    company.is_active = not overdue_payments
    company.save()

    users = User.objects.filter(company_id=company_id)
    users.update(is_active=company.is_active)