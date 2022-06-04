import random
import string
from django.conf import settings
from django.core.cache import cache

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


def unique_order_id_generator(instance):
	order_new_id= random_string_generator()

	Klass= instance.__class__

	qs_exists= Klass.objects.filter(order_id= order_new_id).exists()
	if qs_exists:
		return unique_order_id_generator(instance)
	return order_new_id


def unique_request_id_generator(instance):
	request_new_id= random_string_generator()

	Klass= instance.__class__

	qs_exists= Klass.objects.filter(request_id= request_new_id).exists()
	if qs_exists:
		return unique_request_id_generator(instance)
	return request_new_id



def random_string_generator_for_subs_id(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


def unique_subs_id_generator(instance):
	subs_new_id= random_string_generator_for_subs_id()

	Klass= instance.__class__

	qs_exists= Klass.objects.filter(subs_id=subs_new_id).exists()
	if qs_exists:
		return unique_subs_id_generator(instance)
	return subs_new_id