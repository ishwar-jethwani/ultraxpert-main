import random
import string
from django.conf import settings
from django.core.cache import cache

def random_string_generator_user(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def random_string_generator_service(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def random_string_generator_plan(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def refer_code_gen(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_user_id_generator(instance):
	user_new_id= random_string_generator_user()

	Klass= instance.__class__

	qs_exists= Klass.objects.filter(user_id=user_new_id).exists()
	if qs_exists:
		return unique_user_id_generator(instance)
	return user_new_id


def unique_service_id_generator_service(instance):
	service_new_id= random_string_generator_service()

	Klass= instance.__class__

	qs_exists= Klass.objects.filter(service_id=service_new_id).exists()
	if qs_exists:
		return unique_service_id_generator_service(instance)
	return service_new_id


def unique_plan_id_generator(instance):
	plan_new_id= random_string_generator_plan()

	Klass= instance.__class__

	qs_exists= Klass.objects.filter(plan_id=plan_new_id).exists()
	if qs_exists:
		return unique_plan_id_generator(instance)
	return plan_new_id


def unique_refrence_code_genraor(instance):
	refrence_code_new = refer_code_gen()
	Klass= instance.__class__
	qs_exists= 	Klass.objects.filter(refer_code=refrence_code_new).exists()
	if qs_exists:
		return unique_plan_id_generator(instance)
	return refrence_code_new
