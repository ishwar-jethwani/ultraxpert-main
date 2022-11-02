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

class TestCreateUserData(APIView):
    def get(self,request):
        prof = ["Python Developer","Django Developer","PHP Developer","Dot Net Developer","QA Engineer","Software Engineer","System Engineer","Cloud Service Engineer","Hardware Engineer","Designer","Graphics Designer","Civil Engineer","Frountend Software Develoer","Backend Software Developer"]
        count = 0
        obj_list = []
        # with transaction.atomic():
        while count<500:
            result = requests.get(url="https://randomuser.me/api/")
            data = result.json()
            fname = str(data["results"][0]["name"]["first"])
            lname = str(data["results"][0]["name"]["last"])
            gender = str(data["results"][0]["gender"]).capitalize()
            country = str(data["results"][0]["location"]["country"])
            email = data["results"][0]["email"]
            mobile  = str(data["results"][0]["phone"])
            p_img = data["results"][0]["picture"]["large"]
            title = random.choice(prof)
            experience = random.randint(2,10)
            education = random.choice(["Under Graduate","Post Graduate"])
            description = f" I am {fname}. I have more than {experience} year of experience in this profession. I am reaching out from Creative Bag Unlimited to inform you about the latest addition of bag.We offer different bags and customise them based on your requirement. I would love to set up a meeting with you to show you our catalogue and give you more information"
            count=count+1
            
           
            try:
                if fname.isalpha()==True and lname.isalpha()==True:
                    user= User(email=email,is_expert=True,username=fname)
                    user.is_superuser = False
                    user.is_staff = False
                    user.set_password(f"@dmin@1234")
                    user.save()
                    user_plan = UserPlans.objects.get(id=1)
                    # profiles = Profile.objects.all().values_list("profile_img",flat=True)
                    # if p_img not in list(profiles):
                    if user is not None:
                        obj= Profile.objects.filter(profile=user)
                        if obj.exists():
                            obj.update(first_name=fname,last_name=lname,gender=gender,country=country,user_plan=user_plan,title=title,description=description,education=education,experience=experience,profile_img=p_img)
                        # obj_list.append(obj)
                        print("added",count)
                    else:
                        return Response(data={"msg":"Probile alredy created"},status=status.HTTP_200_OK)
                else:
                    pass
            except IntegrityError as e:
                print(e)
                pass
            
            # try:
            #     Profile.objects.bulk_create(obj_list)
            # except IntegrityError as e:
            #     print(e)
            #     pass
        return Response(data={"msg":"data_created"},status=status.HTTP_201_CREATED)



class TestServiceCreate(APIView):
    def get(self,request):
        prof = ["Python Developer","Django Developer"]
        user_prof = Profile.objects.filter(title__in=prof).values_list("id",flat=True)
        user = User.objects.filter(id__in=list(user_prof))
        category = Category.objects.get(id=21)
        with open("datascripts\data\service.json","r") as file:
            data = file.read()
            file_data  = json.loads(data)
            for data in file_data:
                try:
                    service = Services.objects.create(
                        user = random.choice(user),
                        service_name=data["service_name"],
                        description=data["description"],
                        price=random.choice(data["price"]),currency=data["currency"],
                        service_type=data["service_type"],
                        service_img=random.choice(data["service_img"])
                        )
                    print("added",service.id)
                except:
                    pass
            return Response({"msg":"added"},status=status.HTTP_200_OK)


class TestQuestion(APIView):
    "Test Question Genration"
    def get(self,request):
        data = requests.get(url="https://quizapi.io/api/v1/questions",headers={"X-Api-Key":"m9Fxp2IeoT26gni6OxNvWVDbtFVEwrbYJiJDUWhf"},params={"category":"Docker"})
        main_list = json.loads(data.text)
        if len(data.text)>0:
            pass
        else:
            data = requests.get(url="https://quizapi.io/api/v1/questions",headers={"X-Api-Key":"m9Fxp2IeoT26gni6OxNvWVDbtFVEwrbYJiJDUWhf"},params={"category":"Docker"})
            main_list = json.loads(data.text)
        with transaction.atomic():
            for main_dict in main_list:
                question = main_dict["question"]
                multiple_answer = main_dict["multiple_correct_answers"]
                options = main_dict["answers"]
                answers = main_dict["correct_answers"]
                test_category = main_dict["category"]
                test = Test.objects.create(
                    question=question,
                    options=options,
                    answers=answers,
                    test_category=test_category,
                    multi_ans = eval(multiple_answer.title())
                )
        return Response(data=data.json())

            
            

    
            
        




