from django.contrib import admin

from .models import User_info, Zodiac, Aspects, Stat_Images, Magnetic_Data

admin.site.register(User_info)
admin.site.register(Zodiac)
admin.site.register(Aspects)
admin.site.register(Stat_Images)
admin.site.register(Magnetic_Data)

