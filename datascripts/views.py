from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from user.models import *
import requests
import random
from django.db import transaction,IntegrityError
class Category_Create(APIView):

    def get(self,request):    
        with open("datascripts\data\cat.json","r") as file:
            data = file.read()
            file_data  = json.loads(data)
            data_list = []
            for data in file_data:
                data["name"]
                data["img"]
                model = Category(name=data["name"],img=data["img"],number=data["number"])
                data_list.append(model)
        created = Category.objects.bulk_create(data_list)
        if created:
            return Response({"msg":"created"},status=status.HTTP_200_OK)
        else:
            return Response({"msg":"not created"},status=status.HTTP_400_BAD_REQUEST)

class CreateUserData(APIView):
    def get(self,request):
        prof = ["Python Developer","Django Developer","PHP Developer","Dot Net Developer","QA Engineer","Software Engineer","System Engineer","Cloud Service Engineer","Hardware Engineer","Designer","Graphics Designer","Civil Engineer","Frountend Software Develoer","Backend Software Developer"]
        count = 0
        obj_list = []
        # with transaction.atomic():
        while count<500:
            result = requests.get(url="https://randomuser.me/api/")
            data = result.json()
            fname = data["results"][0]["name"]["first"]
            lname = data["results"][0]["name"]["last"]
            gender = str(data["results"][0]["gender"]).capitalize()
            country = str(data["results"][0]["location"]["country"])
            email = data["results"][0]["email"]
            mobile  = str(data["results"][0]["phone"])
            p_img = data["results"][0]["picture"]["large"]
            title = random.choice(prof)
            experience = random.randint(2,10)
            education = "Under Graduate"
            description = f" I am {fname}. I have more than {experience} year of experience in this profession. I am reaching out from Creative Bag Unlimited to inform you about the latest addition of bag.We offer different bags and customise them based on your requirement. I would love to set up a meeting with you to show you our catalogue and give you more information"
            count=count+1
            try:
                user= User(email=email,is_expert=True,username=fname)
                user.is_superuser = False
                user.is_staff = False
                user.set_password(f"@dmin@1234")
                user.save()
                user_plan = UserPlans.objects.get(id=1)
                if user is not None:
                    obj= Profile.objects.filter(profile=user).update(first_name=fname,last_name=lname,gender=gender,country=country,user_plan=user_plan,title=title,description=description,education=education,experience=experience,profile_img=p_img)
                    # obj_list.append(obj)
                    print("added")
                else:
                    return Response(data={"msg":"Probile alredy created"},status=status.HTTP_200_OK)
            except IntegrityError as e:
                print(e)
                pass
            # try:
            #     Profile.objects.bulk_create(obj_list)
            # except IntegrityError as e:
            #     print(e)
            #     pass
        return Response(data={"msg":"data_created"},status=status.HTTP_201_CREATED)






