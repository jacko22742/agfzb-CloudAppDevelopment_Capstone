from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(max_length=280)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    #constant for c_type choices
    TYPES = (
            ("SEDAN", "Sedan"), ("SUV", "SUV"), ("WAGON", "Wagon"), ("HATCHBACK", "Hatchback"), ("CUPE", "cupe")
        )

    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30)
    c_type = models.CharField(max_length=30, choices=TYPES)
    dealer_id = models.IntegerField()
    year = models.DateField()

    def __str__(self):
        return "Name: " + self.name + \
                " Make Name: "+ self.make.name + \
                " Type: " + self.c_type + \
                " Dealer ID: " + str(self.dealer_id)+ \
                " Year: " + str(self.year)