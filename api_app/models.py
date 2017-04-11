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

class Ward(models.Model):
    """A regional ward, associated with a particular local authority.
    Attributes:
    name: The ward's official name (max. length 50).
    local_authority: Foreign key to the LocalAuthority that the ward is located in.    
    """
    
    name = models.CharField(max_length=100)
    local_authority = models.ForeignKey('LocalAuthority',
                                        on_delete=models.CASCADE)
    class Meta:
        unique_together = (('name','local_authority'),)
        
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

class CountPoint(models.Model):
    """A location at which an AADF count has been made.
    Attributes:
    reference: A numeric ID given to the count point (*not* unique!)
    local_authority: Foreign key to the council Ward responsible for the location.
    road: Foreign key to the Road where the count was taken.
    easting, northing: Map co-ordinates of the location (unique together).
    start_junction: Foreign key to the Junction at the start of the link (may be null).
    end_junction: Foreign key to the Junction at the end of the link (may be null).
    link_length: The length of the link (in kilometres).
    """
    reference = models.IntegerField()
    ward = models.ForeignKey('Ward',
                             on_delete=models.CASCADE)    
    road = models.ForeignKey('Road',
                             on_delete=models.CASCADE)
    easting = models.IntegerField()
    northing = models.IntegerField()
    start_junction = models.ForeignKey('Junction',
                                       related_name='road_starts',
                                       null=True,
                                       on_delete=models.CASCADE)
    end_junction = models.ForeignKey('Junction',
                                     related_name='road_ends',
                                     null=True,
                                     on_delete=models.CASCADE)
    link_length = models.FloatField()

    class Meta:
        # Unfortunately there are odd exceptions where any of these fields can be
        # different between years for a given count point reference. Treat each one
        # as a different count point (in reality would probably do some cleaning up
        # of the data).
        unique_together = (('reference', 'road', 'easting', 'northing',
                            'start_junction', 'end_junction'),)


class TrafficCount(models.Model):
    """A count that occured at a particular count point for a particular year.
    Attributes:
    count_point: Foreign key to the CountPoint where the count was made.
    year: The year when the count was made.
    estimated: Whether the count was an estimate or not.
    estimation_method: The method used for estimation (or counting).
    Various vehicle counts.
    """
    count_point = models.ForeignKey('CountPoint',
                                    on_delete=models.CASCADE)
    year = models.IntegerField()
    estimated = models.BooleanField()
    estimation_method = models.ForeignKey('EstimationMethod',
                                          on_delete=models.CASCADE)
    count_cycles = models.IntegerField()
    count_motorcycles = models.IntegerField()
    count_cars = models.IntegerField()
    count_buses = models.IntegerField()
    count_lightgoods = models.IntegerField()
    count_hgv_2ax_rigid = models.IntegerField()
    count_hgv_3ax_rigid = models.IntegerField()
    count_hgv_45ax_rigid = models.IntegerField()
    count_hgv_34ax_artic = models.IntegerField()
    count_hgv_5ax_artic = models.IntegerField()
    count_hgv_6plus_artic = models.IntegerField()
    
    class Meta:
        unique_together = (('count_point', 'year'),)
