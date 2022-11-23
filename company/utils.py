import random
import string
from django.conf import settings
from django.core.cache import cache

def random_string_training_generator(size=10,chars=string.ascii_lowercase+string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_training_id_generator(instance):
	"""This will genrate new Trinaing ID That will be unique"""
	taininig_new_id= random_string_training_generator()

	Klass= instance.__class__

	qs_exists= Klass.objects.filter(training_id=taininig_new_id).exists()
	if qs_exists:
		return unique_training_id_generator(instance)
	return taininig_new_id

# This is For Company Id Genration 
def random_string_company_generator(size=10,chars=string.ascii_uppercase+string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_company_id_generator(instance):
	"""This will genrate new CompanyID That will be unique"""
	company_new_id= random_string_company_generator()

	Klass= instance.__class__

	qs_exists= Klass.objects.filter(company_id=company_new_id).exists()
	if qs_exists:
		return unique_company_id_generator(instance)
	return company_new_id


# This is For Employee Id Genration 
def random_string_empid_generator(size=5,chars=string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_employee_id_generator(instance):
	"""This will genrate new EmployeeID That will be unique"""
	employee_new_id = unique_employee_id_generator()

	Klass= instance.__class__

	qs_exists= Klass.objects.filter(employee_id=employee_new_id).exists()
	if qs_exists:
		return unique_employee_id_generator(instance)
	return employee_new_id
