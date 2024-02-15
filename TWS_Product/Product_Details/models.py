from django.db import models

# Create your models here.

class Product(models.Model):
    id = models.AutoField(primary_key = True)
    title =  models.CharField(max_length = 255, null = True)
    description =  models.TextField(null = True)
    price =  models.CharField(max_length = 255, null = True)
    created_date = models.DateTimeField(null = True)
    updated_date = models.DateTimeField(null = True)
    retrieval_counts = models.IntegerField(default=1)

    class Meta:
        db_table = 'Product'
