from django.contrib import admin
from .models import Candle

#Changing the site heders and titles
admin.site.site_header = ":::Trading Project Admin:::"
admin.site.site_title = "TRADING PROJECT"
admin.site.index_title = "Candles Data"

# Register your models here.
admin.site.register(Candle)