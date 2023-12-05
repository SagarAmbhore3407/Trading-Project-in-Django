from django.db import models

# Create your models here.
class Candle(models.Model):
    
    symbol = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10 ,decimal_places=2)
    volume = models.CharField(max_length=60)
    
    class Meta:
        app_label = 'MainApp'