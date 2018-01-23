from django.db import models
from django.utils import timezone

class User(models.Model):

	user_name = models.CharField(max_length=200, null=True)
	user_password = models.CharField(max_length=200, null=True)
	user_contact = models.CharField(max_length=200, null=True)
	user_email = models.EmailField(max_length=254, null=True)
	user_country = models.CharField(max_length=200, null=True)
	user_country_name = models.CharField(max_length=200, null=True)
	item_totals = models.CharField(max_length=200, null=True)
	item_quantities = models.CharField(max_length=200, null=True)
	item_indexes = models.CharField(max_length=200, null=True)
	item_descriptions = models.CharField(max_length=200, null=True)

	def time_under_timezone():
		return timezone.localtime(timezone.now())
	item_delivery = models.DateTimeField('Date of Delivery', default=time_under_timezone)

	user_ip = models.CharField(max_length=200, default=0)


	def __str__(self):
		return self.user_name

	def __str__(self):
		return self.user_password

	def __str__(self):
		return self.user_contact
			
	def __str__(self):
		return self.user_email

	def __str__(self):
		return self.user_country

	def __str__(self):
		return self.user_country_name

	def __str__(self):
		return self.item_totals

	def __str__(self):
		return self.item_quantities

	def __str__(self):
		return self.item_indexes

	def __str__(self):
		return self.item_descriptions

	def __str__(self):
		return self.user_ip

'''
class Grocery(models.Model):
	
	user_name = models.CharField(max_length=200)
	user_last_name = models.CharField(max_length=200)
	user_password = models.CharField(max_length=200)
	user_contact = models.CharField(max_length=200)
	user_email = models.EmailField(max_length=254)


	def __str__(self):
		return self.user_name
		
	def __str__(self):
		return self.user_password
		
	def __str__(self):
		return self.user_contact
				
	def __str__(self):
		return self.user_email


class Cart(models.Model):

	def time_under_timezone():
		return timezone.localtime(timezone.now())
	
	user_reference = models.ForeignKey(User, on_delete=models.CASCADE)
	book_reference = models.CharField(max_length=255)
	
	book_author = models.CharField(max_length=255)
	book_description = models.TextField()
	book_image_link = models.CharField(max_length=255)
	book_overview = models.CharField(max_length=255)
	book_reader = models.CharField(max_length=255)
	book_author_reference = models.CharField(max_length=255)
	book_gender = models.CharField(max_length=255)
	book_gender_id = models.CharField(max_length=255)

	date_of_acquisition = models.DateTimeField('Date Acquired', default=time_under_timezone)
	date_of_purchase = models.DateTimeField('Date Purchased', default=time_under_timezone)
	
	book_title = models.CharField(max_length=255)
	
	def __str__(self):
		return self.book_reference
		
	def __str__(self):
		return self.book_author
		
	def __str__(self):
		return self.book_description
		
	def __str__(self):
		return self.book_image_link
		
	def __str__(self):
		return self.book_overview
		
	def __str__(self):
		return self.book_reader
		
	def __str__(self):
		return self.book_gender
		
	def __str__(self):
		return self.book_title
'''
