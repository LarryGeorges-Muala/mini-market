from website.models import User, Grocery, Customer

def format_saved_lists(x):
	if x:
		x = x[1:-1]
		x = x.translate({ord(c): None for c in '"'})
		x = x.split(',')
	return x

def generate_total_items_users_carts():
	total_in_cart = 0
	if User.objects.all():
		for data in User.objects.all():
			if data.item_quantities:
				formatted_cart = format_saved_lists(data.item_quantities)
				for i in range(0, len(formatted_cart)):
					if (i == 1) or (i % 2 == 1):
						total_in_cart += int(formatted_cart[i])
	return total_in_cart

def generate_total_items_users_purchases():
	total_in_purchase = 0
	if User.objects.all():
		for data in User.objects.all():
			if data.customer_set.all():
				for customer in data.customer_set.all():
					formatted_cart = format_saved_lists(customer.item_quantities)
					for i in range(0, len(formatted_cart)):
						if (i == 1) or (i % 2 == 1):
							total_in_purchase += int(formatted_cart[i])
	return total_in_purchase

def generate_total_value_of_users_carts():
	total_in_cart = 0.0
	if User.objects.all():
		for data in User.objects.all():
			if data.item_totals:
				total_in_cart += float(data.item_totals)
	return total_in_cart

def generate_total_value_of_users_purchases():
	total_in_purchase = 0.0
	if User.objects.all():
		for data in User.objects.all():
			if data.customer_set.all():
				for customer in data.customer_set.all():
					total_in_purchase += float(customer.item_totals)
	return total_in_purchase

def generate_occurences():
	per_cart = {}
	if Grocery.objects.all():
		for item in Grocery.objects.all():
			list_to_hold_cart_count = 0
			if User.objects.all():
				for data in User.objects.all():
					if data.item_quantities:
						formatted_cart = format_saved_lists(data.item_quantities)
						if item.name in formatted_cart:
							index_of_item = formatted_cart.index(item.name)
							list_to_hold_cart_count += int(formatted_cart[index_of_item + 1])
			per_cart[item.name] = list_to_hold_cart_count
	return per_cart

def generate_purchase_occurences():
	per_purchase = {}
	if Grocery.objects.all():
		for item in Grocery.objects.all():
			list_to_hold_purchase_count = 0
			if User.objects.all():
				for data in User.objects.all():
					if data.customer_set.all():
						for customer in data.customer_set.all():
							formatted_cart = format_saved_lists(customer.item_quantities)
							if item.name in formatted_cart:
								index_of_item = formatted_cart.index(item.name)
								list_to_hold_purchase_count += int(formatted_cart[index_of_item + 1])
			per_purchase[item.name] = list_to_hold_purchase_count
	return per_purchase

def generate_purchase_table():
	per_purchase = {}
	item_table = generate_occurences()
	purchase_table = generate_purchase_occurences()
	if item_table:
		for cart_key, cart_value in item_table.items():
			per_purchase[cart_key] = {'cart': cart_value, 'purchase': purchase_table[cart_key]}
	return per_purchase

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

def generate_popular_purchases():
	purchase_occurences = generate_purchase_occurences()
	popular_items = {
		'most': {'name': '', 'value': 0},
		'least': {'name': '', 'value': 0}
	}
	if purchase_occurences:
		keys_list = []
		values_list = []
		for keys, values in purchase_occurences.items():
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
