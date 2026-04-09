import datetime
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User

def track_user_interactions(request):
    if request.user.is_authenticated:
        user = request.user
        session = Session.objects.get(session_key=request.session.session_key)
        now = datetime.datetime.now()
        
        
        interaction, created = UserInteraction.objects.get_or_create(
            user=user,
            session=session,
            defaults={
                'last_interaction': now
            }
        )
        if not created:
            interaction.last_interaction = now
            interaction.save()

class UserInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    last_interaction = models.DateTimeField()