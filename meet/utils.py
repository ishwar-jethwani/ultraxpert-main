import random
import string

#Random String Generator 

def random_string_generator_meeting(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# Unique Meeting Id Generator 

def unique_meeting_id_generator(instance):
	meeting_new_id= random_string_generator_meeting()

	Klass= instance.__class__

	qs_exists= Klass.objects.filter(meeting_id=meeting_new_id).exists()
	if qs_exists:
		return unique_meeting_id_generator(instance)
	return meeting_new_id