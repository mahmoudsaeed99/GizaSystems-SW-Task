from django.db import models

# Create your models here.

class Simulator(models.Model):
    startDate = models.DateField()
    endDate = models.DateField(default='')
    dataSize = models.IntegerField(default = 0)
    name = models.CharField(max_length=25)
    timeSeries_CHOICES = [
    ("multiplicative", "multiplicative"),
    ("additive", "additive"),
]
    producer_CHOICES = [
    ("csv", "csv"),
    ("xml", "xsml"),
    ("sql","sql")
]
    timeSeries_type = models.CharField(max_length=25 ,choices=timeSeries_CHOICES , default="additive")
    metaData = models.CharField(max_length=100 , default='' )
    producer_type = models.CharField(max_length=25,choices=producer_CHOICES )
    process_id = models.IntegerField(null=True)
    status = models.CharField(max_length=25,default='Added')




class DataConfig(models.Model):
    frequency = models.CharField(max_length=5)
    noiseLevel = models.IntegerField()
    trendCoef = models.CharField(max_length=15,default='')
    missingPercent = models.DecimalField(max_digits=5 , decimal_places=3)
    outlierPercent = models.IntegerField(default=0)
    timeSeries_CHOICES = [
    (1, 1),
    (0,0),
]
    cycle_amplitude = models.IntegerField(choices=timeSeries_CHOICES)
    cycle_frequency = models.IntegerField()
    simulater = models.ForeignKey(Simulator , on_delete=models.CASCADE , related_name='dataConfig')



class Component(models.Model):
    amplitude = models.IntegerField()
    phase_shift = models.IntegerField()
    frequencyType = [
        ("Daily","Daily"),
        ("Weekly","Weekly"),
        ("Monthly","Monthly")
    ]
    frequency = models.CharField(max_length=10 , choices=frequencyType , default="Daily")
    multiplier = models.IntegerField(default=0)
    dataconfig = models.ForeignKey(DataConfig , on_delete=models.CASCADE , related_name='components')





