from django_extensions.db.fields import AutoSlugField
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib import admin
from django import forms

class Product(models.Model):
	slug = AutoSlugField(('slug'), max_length=60, unique=True, populate_from=('title','created'))
	title = models.CharField(max_length=200)
	description = models.TextField()
	price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(10.00)])
	sale_price = models.DecimalField(decimal_places=2, max_digits=100,\
												null=True, blank=True)
	active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

class VariationManager(models.Manager):
	def all(self):
		return super(VariationManager, self).filter(active=True)

	def sizes(self):
		return self.all().filter(category='size').filter(active=True)

	def colors(self):
		return self.all().filter(category='color').filter(active=True)

VAR_CATEGORIES = (
	('color', 'color'),
	('size', 'size'),
	)

class ProductVariation(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	category = models.CharField(max_length=120, choices=VAR_CATEGORIES, default='color')
	title = models.CharField(max_length=120)
	# image = models.ForeignKey(ProductImage, null=True, blank=True, on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=100, decimal_places=2, null=True, blank=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	active = models.BooleanField(default=True)
	objects = VariationManager()

	def __str__(self):
		return "<variation: %s - %s>" % (self.product.title, self.title)
	
	def save(self):
		if self.category == 'color':
			if self.price:
				print("error")
			else:
				super(ProductVariation, self).save()
		else:
			super(ProductVariation, self).save()

class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	variations = models.ForeignKey(ProductVariation, null=True, blank=True, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='images/')
	active = models.BooleanField(default=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return "<Image: %d - %s>" % (self.product_id, self.product.title)

	def save(self):
		if self.variations:
			if self.variations.category == 'color':
				super(ProductImage, self).save()
			else:
				print("error")
		else:
			super(ProductImage, self).save()

class ProductImageForm(forms.ModelForm):

    class Meta:
        model = ProductImage
        exclude = ['active']

class ProductImageAdmin(admin.ModelAdmin):
	form = ProductImageForm
	list_display = ('product', 'image')