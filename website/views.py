from django.shortcuts import render
from django.http import HttpResponseRedirect
try:
	from django.urls import reverse
except:
	from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template, render_to_string
from django.template import Context
import requests
from ipware import get_client_ip
from django.http import JsonResponse
from website.models import User, Grocery
from django.utils import timezone
from website import default_items

import requests
from bs4 import BeautifulSoup

from htmlmin.decorators import minified_response


def format_saved_lists(x):
	if x:
		x = x[1:-1]
		x = x.translate({ord(c): None for c in '"'})
		x = x.split(',')
	return x

def initialize_groceries():
	products_to_display = []
	for data in Grocery.objects.all():
		products_to_display.append(data.initialize_item_for_display())
	return products_to_display

@minified_response
def index(request):

	if request.method == 'POST':
		captured_name = request.POST.get('name', '')
		captured_email = request.POST.get('email', '')

		captured_country = request.POST.get("country-thing", '')
		starting_clip = captured_country.find('flag')
		ending_clip = captured_country.find('"><')
		captured_country = captured_country[starting_clip:ending_clip].split('-')[1]

		captured_country_name = request.POST.get("country-thing", '')
		captured_country_name = captured_country_name[captured_country_name.find('</i>'):].split('</i>')[1]
		
		#send_simple_message()
		try:
			ip, is_routable = get_client_ip(request)
			if ip is not None:
				id_user, creation_status = User.objects.get_or_create(user_ip=ip)
				id_user.user_name = captured_name
				id_user.user_email = captured_email
				id_user.user_country = captured_country
				id_user.user_country_name = captured_country_name
				
				id_user.item_totals = None
				id_user.item_quantities = None
				id_user.item_indexes = None
				id_user.item_descriptions = None
				
				id_user.save()

			''' Scrap location '''
			##Delivery time scrapping
			delivery_time = ''
			todays_date = timezone.localtime(timezone.now())
			purchase_date = timezone.localtime(timezone.now())

			try:
				url = "http://www.travelmath.com/flying-time/from/Paris,+France/to/" + str(id_user.user_country_name)				
				r = requests.get(url)
				soup = BeautifulSoup(r.text, "html.parser")
				delivery_time = soup.select_one('h3.space').string
				todays_date = todays_date + timezone.timedelta(hours=int(delivery_time.split()[0]))
				todays_date = todays_date + timezone.timedelta(minutes=int(delivery_time.split()[2]))
				delivery_time = todays_date
				id_user.item_delivery = delivery_time
				id_user.save()

			except Exception as error:
				print(error)
				#Default time France - SA
				todays_date = todays_date + timezone.timedelta(hours=11)
				todays_date = todays_date + timezone.timedelta(minutes=33)
				delivery_time = todays_date
				id_user.item_delivery = delivery_time
				id_user.save()
			
			return HttpResponseRedirect('/contact_frame/email-sent/')
		except Exception as error:
			print(error)
			return HttpResponseRedirect('/contact_frame/error-sent/')
		
	''' Init IP recording '''
	ip = None
	is_routable = None
	id_user = None
	creation_status = None
	saved_total_of_items = None
	saved_quantities_of_items = None
	saved_indexes_of_items = None
	saved_description_of_items = None
	
	try:
		ip, is_routable = get_client_ip(request)

		if ip is None:
			print('No IP found')
		else:
			print('IP Address is: ', ip)
			try:
				id_user, creation_status = User.objects.get_or_create(user_ip=ip)
				saved_total_of_items = id_user.item_totals
				saved_quantities_of_items = id_user.item_quantities
				saved_indexes_of_items = id_user.item_indexes
				saved_description_of_items = id_user.item_descriptions
			except Exception as error:
				print(error)

			if is_routable:
				pass
				# The client's IP address is publicly routable on the Internet
			else:
				pass
				# The client's IP address is private
	except Exception as error:
		print(error)

	context = {
		'id_user': id_user,
		'creation_status': creation_status,
		'products_to_display': initialize_groceries(),
		'products_to_display_by_default': default_items.products_to_display_by_default,
		'saved_total_of_items': saved_total_of_items,
		'saved_quantities_of_items': format_saved_lists(saved_quantities_of_items),
		'saved_indexes_of_items': format_saved_lists(saved_indexes_of_items),
		'saved_description_of_items': format_saved_lists(saved_description_of_items),
	}
	return render(request, 'website/index.html', context)


@minified_response
def frame_form(request):
	''' Init IP recording '''
	id_user = None
	try:
		ip, is_routable = get_client_ip(request)
		if ip is not None:
			id_user, creation_status = User.objects.get_or_create(user_ip=ip)
	except Exception as error:
		print(error)
	context = {'client': id_user}
	return render(request, 'website/sheet_frame.html', context)

def generate_total_items_users_carts():
	total_in_cart = 0
	if User.objects.all():
		for data in User.objects.all():
			formatted_cart = format_saved_lists(data.item_quantities)
			for i in range(0, len(formatted_cart)):
				if (i == 1) or (i % 2 == 1):
					total_in_cart += int(formatted_cart[i])
	return total_in_cart

def generate_total_value_of_users_carts():
	total_in_cart = 0.0
	if User.objects.all():
		for data in User.objects.all():
			total_in_cart += float(data.item_totals)
	return total_in_cart

def generate_occurences():
	per_cart = {}
	if Grocery.objects.all():
		for item in Grocery.objects.all():
			list_to_hold_cart_count = 0
			if User.objects.all():
				for data in User.objects.all():
					formatted_cart = format_saved_lists(data.item_quantities)
					if item.name in formatted_cart:
						index_of_item = formatted_cart.index(item.name)
						list_to_hold_cart_count += int(formatted_cart[index_of_item + 1])
			per_cart[item.name] = list_to_hold_cart_count
	return per_cart

def generate_popular_item():
	cart_occurences = generate_occurences()
	popular_items = {
		'most': {'name': '', 'value': 0},
		'least': {'name': '', 'value': 0}
	}
	if cart_occurences:
		keys_list = []
		values_list = []
		for keys, values in cart_occurences.items():
			keys_list.append(keys)
			values_list.append(int(values))

		index_of_highest_value = values_list.index(max(values_list))
		index_of_lowest_value = values_list.index(min(values_list))
		most_popular = keys_list[index_of_highest_value]
		least_popular = keys_list[index_of_lowest_value]

		popular_items['most']['name'] = most_popular
		popular_items['most']['value'] = max(values_list)
		popular_items['least']['name'] = least_popular
		popular_items['least']['value'] = min(values_list)
	return popular_items

@minified_response
def manager(request):
	''' Init IP recording '''
	id_user = None
	try:
		ip, is_routable = get_client_ip(request)
		if ip is not None:
			id_user, creation_status = User.objects.get_or_create(user_ip=ip)
	except Exception as error:
		print(error)

	context = {
		'client': id_user, 
		'grocery_list': Grocery.objects.all(),
		'all_users': User.objects.all(),
		'visitors': User.objects.all().exclude(user_email__contains='@'),
		'registered_users': User.objects.filter(user_email__contains='@'),
		'all_items_in_carts': generate_total_items_users_carts(),
		'total_value_of_carts': generate_total_value_of_users_carts(),
		'item_table': generate_occurences(),
		'popular_items': generate_popular_item()
		}
	return render(request, 'website/manager.html', context)


def totalizer(request):

	total_of_items = request.GET.get('totalOfItems', None)
	quantities_of_items = request.GET.get('quantitiesOfItems', None)
	indexes_of_items = request.GET.get('indexesOfItems', None)
	description_of_items = request.GET.get('descriptionOfItems', None)

	''' Init IP recording '''
	try:
		ip, is_routable = get_client_ip(request)
		if ip is not None:
			id_user, creation_status = User.objects.get_or_create(user_ip=ip)
			id_user.item_totals = total_of_items
			id_user.item_quantities = quantities_of_items
			id_user.item_indexes = indexes_of_items
			id_user.item_descriptions = description_of_items
			id_user.save()
	except Exception as error:
		print(error)

	print()
	print('Data Passed: ')
	print('Total of items: ', total_of_items)
	print('Quantities of items: ', quantities_of_items)
	print('Indexes of items: ', indexes_of_items)
	print('Description of items: ', description_of_items)
	print()

	data = {
		'is_taken': True
	}
	return JsonResponse(data)
