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


class Grocery(models.Model):
	
	name = models.CharField(max_length=200)
	price = models.CharField(max_length=200)
	quantity = models.IntegerField(default=0)
	
	url = models.ImageField(upload_to='groceries', default='', null=True)

	def __str__(self):
		return self.url

	def initialize_item_for_display(self):
		temporary_dict = {
			'name': self.name,
			'price': self.price,
			'quantity': self.quantity,
			'url': '/media/' + str(self.url) if self.url else self.url,
		}
		return temporary_dict

	def __str__(self):
		return self.name


class Customer(models.Model):
	
	user_reference = models.ForeignKey(User, on_delete=models.CASCADE)
	item_totals = models.CharField(max_length=200, null=True)
	item_quantities = models.CharField(max_length=200, null=True)
	item_indexes = models.CharField(max_length=200, null=True)
	item_descriptions = models.CharField(max_length=200, null=True)

	def time_under_timezone():
		return timezone.localtime(timezone.now())
	item_delivery = models.DateTimeField('Date of Delivery', default=time_under_timezone)
	purchase_date = models.DateTimeField('Date of Purchase', default=time_under_timezone)

	def prepare_for_display(self):
		items_dict = {}
		if self.item_quantities:
			x = self.item_quantities
			x = x[1:-1]
			x = x.translate({ord(c): None for c in '"'})
			x = x.split(',')
			for i in range(0, len(x)):
				if (i == 1) or (i % 2 == 1):
					pass
				else:
					items_dict[x[i]] = x[i+1]
		return items_dict

	def prepare_delivery_status(self):
		if self.item_delivery > timezone.localtime(timezone.now()):
			return 'in progress'
		return 'delivered'
			

	def __str__(self):
		return self.item_totals

	def __str__(self):
		return self.item_quantities

	def __str__(self):
		return self.item_indexes

	def __str__(self):
		return self.item_descriptions

	def __str__(self):
		return self.user_reference
