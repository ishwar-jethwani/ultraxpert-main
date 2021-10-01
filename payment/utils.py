import random
import string

def random_string_generator_for_payment_id(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


def unique_payment_id_generator(instance):
	payment_new_id= random_string_generator_for_payment_id()

	Klass= instance.__class__

	qs_exists= Klass.objects.filter(payment_id=payment_new_id).exists()
	if qs_exists:
		return unique_payment_id_generator(instance)
	return payment_new_id