from rest_framework import serializers
from user.models import User
from django.contrib.auth import authenticate


class UserSerilizer(serializers.ModelSerializer):
    class Meta:
        fields = ["pk","user_id","is_expert","is_verified","username","email","mobile"]
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
            
        
        