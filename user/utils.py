import random
import string
from django.conf import settings
from django.core.cache import cache

# This is For User Id Genration 
def random_string_generator_user(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_user_id_generator(instance):
	"""This will genrate new UserID That will be unique"""
	user_new_id= random_string_generator_user()

	Klass= instance.__class__

	qs_exists= Klass.objects.filter(user_id=user_new_id).exists()
	if qs_exists:
		return unique_user_id_generator(instance)
	return user_new_id

# This is for service id Genration
def random_string_generator_service(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_service_id_generator_service(instance):
	"""This will genrate new service id that will be unique"""
	service_new_id= random_string_generator_service()

	Klass= instance.__class__

	qs_exists= Klass.objects.filter(service_id=service_new_id).exists()
	if qs_exists:
		return unique_service_id_generator_service(instance)
	return service_new_id

# This is for user Plan id genration
def random_string_generator_plan(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))
	
def unique_plan_id_generator(instance):
	"""This will genrate user plan id that will be unique"""
	plan_new_id= random_string_generator_plan()

	Klass= instance.__class__

	qs_exists= Klass.objects.filter(plan_id=plan_new_id).exists()
	if qs_exists:
		return unique_plan_id_generator(instance)
	return plan_new_id


# This is for user Plan id genration

def refer_code_gen(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_refrence_code_genrator(instance):
	"""This will genrate refrence code  that will be unique"""
	refrence_code_new = refer_code_gen()
	Klass= instance.__class__
	qs_exists= 	Klass.objects.filter(refer_code=refrence_code_new).exists()
	if qs_exists:
		return unique_refrence_code_genrator(instance)
	return refrence_code_new

#This is for user test id genration
def user_test_id_genrator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_test_id_gen(instance):
	"""This will genrate user test id that will be unique"""
	test_id = user_test_id_genrator()
	Klass= instance.__class__
	qs_exists= 	Klass.objects.filter(test_id=test_id).exists()
	if qs_exists:
		return unique_test_id_gen(instance)
	return test_id








