from django.contrib import admin

# Register your models here.
from appinventories.models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ("nombre", "marca","cantidad", "fechaAlta", "fechaBaja")
    search_fields = ("nombre", "marca")
    list_filter = ("fechaAlta","fechaBaja")
    date_hierarchy=("fechaAlta")

admin.site.register(Product,ProductAdmin)
