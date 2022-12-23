from django.contrib import admin
from . models import CustomUser,Profile,blockusers

class customuserAdmin(admin.ModelAdmin):
    list_display=('username','first_name','last_name','email','phone')
class user_sddress2Admin(admin.ModelAdmin):
    list_display=('fist_name','last_name')


# Register your models here.
admin.site.register(CustomUser,customuserAdmin)
admin.site.register(Profile)
admin.site.register(blockusers)