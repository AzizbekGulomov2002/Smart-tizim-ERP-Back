from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from apps.users.models import Company, User
from rest_framework.decorators import api_view
from datetime import date
from django.utils import timezone


@api_view(['GET'])
def company_off_view(request):
    companies = Company.objects.all()
    now = timezone.now().date()
    response_data = []

    for company in companies:
        if company.end_date <= now:
            print("Today: ",now)
            print("End date: ",company.end_date)
            company.is_active = False
            print("Company name : ",company.comp_name,company.is_active)
            company.save()
            users = User.objects.filter(company_id=company.id)
            for user in users:
                print("Username: ",user.username, user.is_active)
                user.is_active = False
                user.save()
            response_data.append({
                "company_id": company.id,
                "status": "Muddati o'tgan"
            })
        else:
            company.is_active = True
            company.save()
            print("Company name : ", company.comp_name, company.is_active)
            users = User.objects.filter(company_id=company.id)
            for user in users:
                user.is_active = True
                user.save()
                print("Username: ", user.username, user.is_active)
            response_data.append({
                "company_id": company.id,
                "status": True
            })

    return Response(response_data, status=status.HTTP_200_OK)



@api_view(['GET'])
def company_on_view(request):
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