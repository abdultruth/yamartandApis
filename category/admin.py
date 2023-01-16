from django.contrib import admin


from .models import Cartegory
# Register your models here.
class CartAdmin(admin.ModelAdmin):
    model = Cartegory
    list_display = ('category_name', 'slug', 'discription')
    prepopulated_fields = {'slug': ('category_name',)}
    
admin.site.register(Cartegory, CartAdmin)
