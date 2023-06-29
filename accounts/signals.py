from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver
from .models import User , UserProfile





@receiver(post_save, sender = User)
def post_save_create_profile_receiver(sender ,instance,created,**kwargs):
    if created:
        # print('create the user profile')
        UserProfile.objects.create(user=instance)
    else:
        try:
            
            profile = UserProfile.objects.get(user= instance)
            profile.save()
            # print('i am in try-block')
        except:
            # Create the user profile if not exist
            UserProfile.objects.create(user = instance)
            # print('user_profile_updated')
        

