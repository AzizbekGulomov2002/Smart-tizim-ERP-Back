from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from apps.users.models import Company, User
from rest_framework.decorators import api_view
from datetime import date
from django.utils import timezone


@api_view(['GET'])
def off_view(request):
    companies = Company.objects.all()
    now = timezone.now().date()
    for company in companies:
        end_date = company.end_date
        if isinstance(end_date, date) and end_date <= now:
            print(company.is_active)
            print(type(company.end_date))
            print(type(now))
            company.is_active = False
            company.save()
            users = User.objects.filter(company_id=company.id)
            for user in users:
                user.is_active = False
                user.save()
    return Response(status=status.HTTP_200_OK)



@api_view(['GET'])
def on_view(request):
    company = Company.objects.all()
    for i in company:
        if i.is_active == True:
            user = User.objects.filter(company_id=i.id)
            for u in user:
                u.is_active = True
                u.save()
    return Response(status=status.HTTP_200_OK)


# @api_view(['GET'])
# def example(request):
#     company = Company.objects.get(id=6)
#     company.is_active = True
#     company.save()
#     return Response(status=status.HTTP_200_OK)