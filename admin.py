from django.contrib import admin
from AdminApp.models import Category, Food


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display= ("id","cat_name")

class FoodAdmin(admin.ModelAdmin):
    list_display=('id','item_name','price','description','imageurl','category')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Food,FoodAdmin)
