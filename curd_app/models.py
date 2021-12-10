from django.db import models

# Create your models here.
class ProductModel(models.Model):
	no = models.IntegerField(primary_key=True)
	name = models.CharField(unique=True, max_length=30)
	price = models.FloatField()
	quantity = models.IntegerField()