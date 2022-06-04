from django.db import models
from user.models import User
from uuid import uuid4
user = User()

def deserialize_user(user):
    """Deserialize user instance to JSON."""
    return {
        'id': user.id,"user_id":user.user_id,'username': user.username, 'email': user.email,
    }

# class Message(models.Model):
#      sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')        
#      receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')        
#      message = models.CharField(max_length=1200)
#      timestamp = models.DateTimeField(auto_now_add=True)
#      is_read = models.BooleanField(default=False)
#      def __str__(self):
#            return self.message
#      class Meta:
#            ordering = ('timestamp',)




class TrackableDateModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def _generate_unique_uri():
    return str(uuid4()).replace('-', '')[:15]


class ChatSession(TrackableDateModel):
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    uri = models.URLField(default=_generate_unique_uri)


class ChatSessionMessage(TrackableDateModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    chat_session = models.ForeignKey(
        ChatSession, related_name='messages', on_delete=models.PROTECT
    )
    message = models.TextField(max_length=2000)

    def to_json(self):
        """deserialize message to JSON."""
        return {'user': deserialize_user(self.user), 'message': self.message}


class ChatSessionMember(TrackableDateModel):
    chat_session = models.ForeignKey(
        ChatSession, related_name='members', on_delete=models.PROTECT
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT)