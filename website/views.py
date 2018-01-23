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
from website.models import User
from django.utils import timezone

import requests
from bs4 import BeautifulSoup

from htmlmin.decorators import minified_response


def format_saved_lists(x):
	if x:
		x = x[1:-1]
		x = x.translate({ord(c): None for c in '"'})
		x = x.split(',')
	return x

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
		"""
		print(captured_name)
		print(captured_email)
		print(captured_number)
		print(captured_enquiry)
		print(captured_msg)
		"""
		
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
		'saved_total_of_items': saved_total_of_items,
		'saved_quantities_of_items': format_saved_lists(saved_quantities_of_items),
		'saved_indexes_of_items': format_saved_lists(saved_indexes_of_items),
		'saved_description_of_items': format_saved_lists(saved_description_of_items),
	}
	return render(request, 'website/index.html', context)

def sheet(request):

	''' Init IP recording '''
	ip, is_routable = get_client_ip(request)
	id_user = None
	creation_status = None

	if ip is None:
		print('No IP found')
	else:
		print('IP Address is: ', ip)

		try:
			id_user, creation_status = User.objects.get_or_create(user_ip=ip)
			print(id_user)
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
	context = {
		'id_user': id_user,
		'creation_status': creation_status,
		'saved_total_of_items': saved_total_of_items,
		'saved_quantities_of_items': format_saved_lists(saved_quantities_of_items),
		'saved_indexes_of_items': format_saved_lists(saved_indexes_of_items),
		'saved_description_of_items': format_saved_lists(saved_description_of_items),
	}
	return render(request, 'website/sheet_app.html', context)

def sheet_angular(request):
	cart_received = '["Fresh Tomatoes",5,"Fresh Apples",2,"Monster Pumpkins",3,"Milky Tart",5]'
	cart_received = cart_received[1:-1]
	cart_received = cart_received.translate({ord(c): None for c in '"'})
	cart_received = cart_received.split(',')
	
	context = {
		'passed_cart': cart_received,
		'passed_total': 329.85,
	}
	return render(request, 'website/sheet_angular.html', context)

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

def validate_username(request):
	username = request.GET.get('username', None)
	print(username)
	data = {
		'is_taken': True
	}
	return JsonResponse(data)

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
