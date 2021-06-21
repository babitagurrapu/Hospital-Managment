from django.db import models
from django.shortcuts import reverse



class City(models.Model):
	"""City is aimed to use as Foreign key for Donor model"""

	name = models.CharField(max_length=50, blank=False, null=False)
	created = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return self.name




class Feedback(models.Model):
	name = models.CharField(max_length=256, blank=False, null=False)
	contact = models.CharField(max_length=1024, blank=False, null=False)
	message = models.TextField()
	IP = models.CharField(max_length=100, blank=True, null=True, default='n/a')
	sent_at = models.DateTimeField(auto_now=False, auto_now_add=True)

	created = models.DateTimeField(auto_now=False, auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)

	def __str__(self):
		return self.message

	@property
	def get_absolute_url(self):
		return reverse('feedback-detail', kwargs={'pk': self.pk})
