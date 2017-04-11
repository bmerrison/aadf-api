from rest_framework import serializers
from api_app.models import Junction, \
    EstimationMethod, \
    Region, \
    LocalAuthority, \
    Ward, \
    RoadCategory, \
    Road, \
    CountPoint, \
    TrafficCount

class JunctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Junction
        fields = ('id', 'description')

class EstimationMethodSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = EstimationMethod
        fields = ('id', 'description', )
        
class RegionSerializer(serializers.ModelSerializer):
    local_authorities = serializers.PrimaryKeyRelatedField(
        many=True,
        default=[],
        queryset=LocalAuthority.objects.all())
        
    class Meta:
        model = Region
        fields = ('id', 'name', 'local_authorities')

class LocalAuthoritySerializer(serializers.ModelSerializer):
    region_name = serializers.ReadOnlyField(source='region.name')
    
    class Meta:
        model = LocalAuthority
        fields = ('id', 'name', 'region', 'region_name')

class WardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ward
        fields = ('id', 'name', 'local_authority')                

class RoadCategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RoadCategory
        fields = ('id', 'code', 'description' )
        
class RoadSerializer(serializers.ModelSerializer):
    category_code = serializers.ReadOnlyField(source='category.code')
    
    class Meta:
        model = Road
        fields = ('id', 'name', 'category', 'category_code' )

class CountPointSerializer(serializers.ModelSerializer):
    road_name = serializers.ReadOnlyField(source='road.name')
    road_category_code = serializers.ReadOnlyField(source='road.category.code')
    ward_name = serializers.ReadOnlyField(source='ward.name')
    local_authority_name = serializers.ReadOnlyField(source='ward.local_authority.name')
    region_name = serializers.ReadOnlyField(source='ward.local_authority.region.name')
    start_junction_desc = serializers.ReadOnlyField(source='start_junction.description')
    end_junction_desc = serializers.ReadOnlyField(source='end_junction.description')
    link_length_miles = serializers.SerializerMethodField('km_to_miles')
    
    def km_to_miles(self, instance):
        return round(instance.link_length / 1.60934, 1)
    
    class Meta:
        model = CountPoint
        fields = ('id', 'reference', 'ward', 'ward_name', 'local_authority_name',
                  'region_name', 'road', 'road_name', 'road_category_code', 'easting',
                  'northing', 'start_junction', 'start_junction_desc', 'end_junction',
                  'end_junction_desc', 'link_length', 'link_length_miles')
        
class TrafficCountSerializer(serializers.ModelSerializer):
    count_point_ref = serializers.ReadOnlyField(source='count_point.reference')
    estimation_details = serializers.ReadOnlyField(source='estimation_method.description')
    count_hgv = serializers.SerializerMethodField('get_hgv_count')
    count_all = serializers.SerializerMethodField('get_all_count')

    def get_hgv_count(self, tc):
        return tc.count_hgv_2ax_rigid + tc.count_hgv_3ax_rigid + tc.count_hgv_45ax_rigid + \
            tc.count_hgv_34ax_artic + tc.count_hgv_5ax_artic + tc.count_hgv_6plus_artic

    def get_all_count(self, tc):
        return self.get_hgv_count(tc) + tc.count_cycles + tc.count_motorcycles + \
            tc.count_cars + tc.count_buses + tc.count_lightgoods
    
    class Meta:
        model = TrafficCount
        fields = ('id', 'count_point', 'count_point_ref', 'year', 'estimated', 'estimation_method', 'estimation_details',
                  'count_cycles', 'count_motorcycles', 'count_cars',
                  'count_buses', 'count_lightgoods', 'count_hgv_2ax_rigid',
                  'count_hgv_3ax_rigid', 'count_hgv_45ax_rigid',
                  'count_hgv_34ax_artic', 'count_hgv_5ax_artic',
                  'count_hgv_6plus_artic', 'count_hgv', 'count_all')
