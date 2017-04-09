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

    name = models.CharField(max_length=100, unique=True)

class LocalAuthority(models.Model):
    """A local authority, located within a region.
    Attributes:
    name: The name of the authority (max. length 100), must be unique within a region.
    region: The Region that the local authority is associated with.
    """    

    name = models.CharField(max_length=100)
    region = models.ForeignKey('Region',
                               related_name='local_authorities',
                               on_delete=models.CASCADE)

    class Meta:
        unique_together = (('name','region'),)

class RoadCategory(models.Model):
    """A code used to describe road types. This would probably be better as
    an enumeration field in Road, but there appears to currently be a bug in
    coreapi when using enums (https://github.com/core-api/python-client/issues/122).
    Attributes:
    code: A two-letter code for the category.
    description: Text describing the category.
    """
    code = models.CharField(max_length=2, unique=True)
    description = models.TextField(unique=True)
    
class Road(models.Model):
    """A road that a count has been performed on.
    Attributes:
    name: The road's name (max. length 20).
    category: The road's Category. name,category pairs must be unique.
    """

    name = models.CharField(max_length=20)
    category = models.ForeignKey('RoadCategory',
                                 related_name='roads',
                                 on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (('name','category'),)
