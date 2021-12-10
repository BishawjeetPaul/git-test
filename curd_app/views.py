from django.shortcuts import render
from django.views.generic import View
from curd_app.models import ProductModel
from django.http import HttpResponse
from django.core.serializers import serialize
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.

# Reading all the products from db and giving as JSON response
# Use Class Based view
class ViewAllProducts(View):
	def get(self, request):
		qs = ProductModel.objects.all()
		data = {}
		for row in qs:
			d1 = {
				row.no: {
					'product_name':row.name,
					'product_price':row.price,
					'product_quantity':row.quantity
				}
			}
			data.update(d1)
		# Converting dict to json
		json_data = json.dumps(data)
		return HttpResponse(json_data, content_type='application/json')


# Serializing Django objects
# Django Serializing framework provides a mechanism for "Translating"
# Django models into other formates

# reading all the products from db and giving as JSON response(dict of dict )
# use class based view
# Note: we are using build in "serializers"


class ViewAllProductsSers(View):
	def get(self, request):
		qs = ProductModel.objects.all()
		json_data = serialize('json',qs)
		return HttpResponse(json_data, content_type="application/json")


# Reading 1 product from db and giving as JSON response using class based view
class ViewOneProduct(View):
	def get(self, request, product):
		try:
			qs = ProductModel.objects.get(no=product)
			data = {
				"product_name": qs.name,
				"product_price": qs.price,
				"product_quantity": qs.quantity
			}
			json_data = json.dumps(data)
		except ProductModel.DoesNotExist:
			error_message = {"error": "Product No is Not Available"}
			json_data = json.dumps(error_message)
		return HttpResponse(json_data, content_type="application/json")

# reading 1 product from db using class based view
# Note: in this we are using django build in serialisers

class ViewOneProductSers(View):
	def get(self, request, product):
		try:
			qs = ProductModel.objects.get(no=product)
			json_data = serialize('json',[qs])
		except ProductModel.DoesNotExist:
			error_message = {"error": "Product No is Not Available"}
			json_data = json.dumps(error_message)
		return HttpResponse(json_data, content_type="application/json")

# Insert One product using class based view
@method_decorator(csrf_exempt, name='dispatch')
class InsertOneProduct(View):
	def post(self, request):
		data = request.body            # Will return binary string.
		data_json = json.loads(data)   # Converts into dictionary.
		p1 = ProductModel.objects.create(no=data_json['no'],name=data_json['name'],\
			price=data_json['price'],
			quantity=data_json['quantity'])
		p1.save()
		json_data = json.dumps({"Success":"Product is Saved"})
		return HttpResponse(json_data, content_type="application/json")


# Update one product using class based view
@method_decorator(csrf_exempt, name='dispatch')
class UpdateOneProduct(View):
	def put(self, request, product):
		new_data = request.body
		new_data_json = json.loads(new_data)
		try:
			qs = ProductModel.objects.get(no=product)
			data = {
				"name":qs.name,
				"price":qs.price,
				"quantity":qs.quantity,
			}
			data.update(new_data_json)
			qs.name = data["name"]
			qs.price = data["price"]
			qs.quantity = data["quantity"]
			qs.save()
			json_message = {"Success":"Product Updated Successfully!"}
		except ProductModel.DoesNotExist:
			json_message = {"error":"Invalid Product"}
		json_data = json.dumps(json_message)
		return HttpResponse(json_data, content_type="application/json")


# Delete One Droduct using class based view
class DeleteOneProduct(View):
	def get(self, request, product):
		try:
			qs = ProductModel.objects.get(no=product).delete()
			json_message = json.dumps({"success":"Product is Deleted!"})
		except ProductModel.DoesNotExist:
			json_message = json.dumps({"error":"Product No. is Not Available"})
		json_data = json.dumps(json_message)
		return HttpResponse(json_data, content_type="application/json")