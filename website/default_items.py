from website.models import Grocery

products_to_display_by_default = [
{ 
    'name': 'Fresh Tomatoes', 
    'price': 5.99, 
    'quantity': 0,
    'url': "{% static 'website/images/resized/tomato-2-compressor.jpg' %}",
},
{ 
    'name': 'Fresh Apples', 
    'price': 5.99, 
    'quantity': 0,
    'url': "{% static 'website/images/resized/apple-2-compressor.jpg' %}",
},
{ 
    'name': 'Monster Pumpkins', 
    'price': 17.99, 
    'quantity': 0,
    'url': "{% static 'website/images/resized/pumpkin-2-compressor.jpg' %}",
},
{ 
    'name': 'Delicious Pitaya', 
    'price': 35.99, 
    'quantity': 0,
    'url': "{% static 'website/images/resized/pitaya-1-compressor.jpg' %}",
},
{ 
    'name': 'French Fries', 
    'price': 12.99, 
    'quantity': 0,
    'url': "{% static 'website/images/resized/fries-1-compressor.jpg' %}",
}, 
{ 
    'name': 'Oriental Salad', 
    'price': 16.99, 
    'quantity': 0,
    'url': "{% static 'website/images/resized/salad-1-compressor.jpg' %}",
},
{ 
    'name': 'Blackberries', 
    'price': 3.99, 
    'quantity': 0,
    'url': "{% static 'website/images/resized/berries-1-compressor.jpg' %}",
},
{ 
    'name': 'Succulent Tart', 
    'price': 35.99, 
    'quantity': 0,
    'url': "{% static 'website/images/resized/tart-1-compressor.jpg' %}",
},
]


def create_default_groceries():
    for data in products_to_display_by_default:
        Grocery.objects.get_or_create(name = data['name'], price = data['price'], quantity = data['quantity'])

'''
try:
    create_default_groceries()
except Exception as error:
    print()
    print(error)
    print()
'''
