from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from allauth.account.signals import user_logged_in, user_signed_up
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your models here.
class profile(models.Model):
	name = models.CharField(max_length=120)
	user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True)
	descriptions = models.TextField(default='description default text')

	def __str__(self):
		return self.name


class userStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    stripe_id = models.CharField(max_length=200, null=True, blank=True)	

    def __str__(self):
    	if self.stripe_id:
    		return str(self.stripe_id)
    	else:
    		return self.user.username

def stripeCallback(sender, request, user, **kwargs):
	user_stripe_account, created = userStripe.objects.get_or_create(user=user)
	if created:
		print ('created for %s'%(user.username))
	if user_stripe_account.stripe_id is None or user_stripe_account.stripe_id =='':
	  	new_stripe_id = stripe.Customer.create(email=user.email)
	  	user_stripe_account.stripe_id = new_stripe_id['id']
	  	user_stripe_account.save()

 
def profileCallback(sender, request, user, **kwargs):
	userProfile, is_created = profile.objects.get_or_create(user=user)
	if is_created:
		userProfile.name = user.username
		userProfile.save()

user_logged_in.connect(stripeCallback)
user_signed_up.connect(profileCallback)



class Track(models.Model):
	title = models.CharField(max_length=20)
	descriptions = models.TextField(max_length=1000)
	def __str__(self):
		return self.title
		pass
    	
   
class Speaker(models.Model):
	name = models.CharField(max_length=20)
	facebook = models.CharField(max_length=20, blank = True)
	twitter = models.CharField(max_length=20, blank = True)
	bio = models.TextField(max_length=1000)
	def __str__(self):
		return self.name
		pass
SESSION_STATUS	 = (
    ('a', 'Approved'),
    ('s', 'Submitted'),
    ('r', 'Rejected')
	)
    
class Session(models.Model):
    title = models.CharField(max_length=20)   
    abstract = models.TextField(max_length=1000)
    speaker = models.ForeignKey(Speaker)
    track = models.ForeignKey(Track)
    status = models.CharField(max_length=1, choices = SESSION_STATUS)
    def __str__(self):
    	return self.title
    from django.db import models





