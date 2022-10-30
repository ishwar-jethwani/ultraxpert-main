from email.policy import default
from rest_framework import serializers
from user.models import User
from dj_rest_auth.registration.serializers import RegisterSerializer

#Custom Registration

class CustomRegisterSerializer(RegisterSerializer):
    reffered_by = serializers.CharField(max_length=10,required=False)    
    verification_status = serializers.BooleanField(default=False)
    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['reffered_by'] = self.validated_data.get('reffered_by', '')
        data_dict["verification_status"] = self.validated_data.get('verification_status')
        return data_dict

#User Selilizer 

class UserSerilizer(serializers.ModelSerializer):
    class Meta:
        fields = ["pk","user_id","is_expert","is_verified","username","email","mobile","refer_code","reffered_by"]
        model = User

#User Order Serilizer
  
class OrderUserSerilizer(serializers.ModelSerializer):
    class Meta:
        fields = ["pk","user_id","is_expert","is_verified","username"]
        model = User








# class MobileUserSerializer(serializers.Serializer):
#     mobile = serializers.CharField()
#     password = serializers.CharField(
#         style={'input_type': 'password'}, trim_whitespace=False)
#     def validate(self, attrs):
#         mobile = attrs.get('mobile')
#         password = attrs.get('password')

#         if mobile and password:
#             if User.objects.filter(mobile=mobile).exists():
#                 user = authenticate(request=self.context.get('request'),
#                                     mobile=mobile, password=password)
                
#             else:
#                 msg = {'detail': 'mobile number is not registered.',
#                        'register': False}
#                 raise serializers.ValidationError(msg)

#             if not user:
#                 msg = {
#                     'detail': 'Unable to log in with provided credentials.', 'register': True}
#                 raise serializers.ValidationError(msg, code='authorization')

#         else:
#             msg = 'Must include "username" and "password".'
#             raise serializers.ValidationError(msg, code='authorization')

#         attrs['user'] = user
#         return attrs
            
        
        