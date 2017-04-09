from django.db import models

class Junction(models.Model):
    """A junction where roads meet. Each count point is between two junctions.
    Attributes:
    description: A unique string (max. length 200) describing the junction.
    """
    
    description = models.CharField(max_length=200, unique=True) 

class EstimationMethod(models.Model):
    """A method of estimating the traffic flow.
    Attributes:
    description: A (potentially long) unique string describing the method.
    """

    description = models.TextField(unique=True) 

class Region(models.Model):
    """A region of the country (contains local authorities).
    Attributes:
    name: A unique string (max. length 100) giving the region's name.
    """

    name = models.TextField(unique=True) 
