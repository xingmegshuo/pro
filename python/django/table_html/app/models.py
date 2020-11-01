from django.db import models

# Create your models here.


class info(models.Model):
    cpu = models.CharField(max_length=50)
    hard_disk = models.CharField(max_length=50)
    video_memory = models.CharField(max_length=50)
    memory = models.CharField(max_length=50)

class Computer(models.Model):
    name = models.CharField(max_length=50)
    number = models.CharField(max_length=20)
    n_type = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    unit_price = models.CharField(max_length=50)
    quantity = models.CharField(max_length=50)
    note = models.TextField(null=True)
    info = models.ForeignKey(info,on_delete=models.CASCADE)



