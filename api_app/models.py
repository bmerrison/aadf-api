from django.db import models

class Junction(models.Model):
    """A junction where roads meet. Each count point is between two junctions.
    Attributes:
    description: A string (max. length 200) describing the junction.
    """
    
    description = models.CharField(max_length=200, unique=True) 

class EstimationMethod(models.Model):
    """A method of estimating the traffic flow.
    Attributes:
    description: A (potentially long) string describing the method.
    """

    description = models.TextField(unique=True) 
