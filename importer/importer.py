import shapefile
from shapely.geometry import Polygon, Point

import coreapi
from coreapi.exceptions import ErrorMessage

import csv, sys
from itertools import count

from util import OSGB36toWGS84

if __name__ == '__main__':
    csv_path = sys.argv[1]
    shapefile_name = sys.argv[2]
    
    # After the CSV file has been read, all_rows will contain a list
    # where each entry is name->value dictionary for a row.
    all_rows = []

    # Load and parse CSV.
    with open(csv_path, 'rt') as f_in:
        csv_reader = csv.reader(f_in)
        col_names = None
        for row in csv_reader:
            if not col_names:
                col_names = row
            else:
                all_rows.append({col: val for col, val in zip(col_names, row)})

    # Load ward geometry for certain local authorities from
    # the ward shapefiles. Restrict to (roughly) only those in the
    # south west, using co-ordinates below.
    min_easting, max_easting = 130687,342000
    min_northing, max_northing = 10380,150750
    sf = shapefile.Reader(shapefile_name)
    field_names = [f[0] for f in sf.fields[1:]]
    records = [{f: v for f, v in zip(field_names, record)} for record in sf.records()]
    ward_polygons = []
    auth_names = []
    for record, shape in zip(records, sf.shapes()):
        easting, northing = int(record['bng_e']), int(record['bng_n'])
        if easting < min_easting or easting > max_easting or \
           northing < min_northing or northing > max_northing:
            continue
        
        auth_name = record['lad16nm']
        if auth_name not in auth_names:
            auth_names.append(auth_name) # Yuck, should use set!

        ward_name = record['wd16nm']
        ward_polygon = Polygon(shape.points)
        ward_polygons.append((ward_polygon, ward_name, auth_name))
    print("Loaded {0} ward shapes from {1}.".format(len(ward_polygons), shapefile_name))

    # Get API schema.
    client = coreapi.Client()
    schema = client.get('http://localhost:8000/schema')

    # Get a set of unique junction descriptions by combining all values from
    # the "StartJunction" and "EndJunction" columns.
    junc_descs = set([r["StartJunction"] for r in all_rows] +
                     [r["EndJunction"] for r in all_rows])
    junc_descs.discard('')
    # junction_ids will contain a mapping from junction description to database ID.
    junction_ids = {}
    print("Importing {0} junctions...".format(len(junc_descs)))
    # Add junctions to the database.
    for junc_desc in junc_descs:
        try:
            resp = client.action(schema,
                                 ['junctions', 'create'],
                                 params={'description': junc_desc})
            junction_ids[junc_desc] = resp.get('id')
        except ErrorMessage as err:
            print("Error adding junction: {0}".format(err.error))
            raise

    # Get a set of unique estimation method descriptions.
    est_method_descs = set([r["Estimation_method_detailed"]
                            for r in all_rows])
    est_method_descs.discard('')
    # est_method_ids will contain a mapping from estimation method description to database ID.
    est_method_ids = {}
    print("Importing {0} estimation methods...".format(len(est_method_descs)))
    # Add estimation methods to the database.
    for est_method_desc in est_method_descs:
        try:
            resp = client.action(schema,
                                 ['estimation_methods', 'create'],
                                 params={'description': est_method_desc})
            est_method_ids[est_method_desc] = resp.get('id')
        except ErrorMessage as err:
            print("Error adding estimation method: {0}".format(err.error))
            raise        

    # Get a set of unique region names.
    region_names = set([r["Region"] for r in all_rows])
    print("Importing {0} regions...".format(len(region_names)))
    # region_ids will contain a mapping of region names to database IDs.
    region_ids = {}
    for region_name in region_names:
        try:
            resp = client.action(schema,
                                 ['regions', 'create'],
                                 params={'name': region_name})
            region_ids[region_name] = resp.get('id')
        except ErrorMessage as err:
            print("Error adding region: {0}".format(err.error))
            raise

    # Get a set of unique (region name, local authority name) pairs.
    # Since I'm getting local authorities from the shapefile, no
    # easy way to get the corresponding region so just hard code South West...
    print("Importing {0} local authorities...".format(len(auth_names)))
    # region_auth_ids will contain a mapping of (region,auth) name
    # pairs to database IDs.
    authority_ids = {}
    for authority_name in auth_names:
        try:
            resp = client.action(schema,
                                 ['local_authorities', 'create'],
                                 params={'name': authority_name,
                                         'region': region_ids['South West']})
            authority_ids[(region_name, authority_name)] = resp.get('id')
        except ErrorMessage as err:
            print("Error adding local authority: {0}".format(err.error))
            raise

    # Add wards to the database. ward_ids will contain a mapping from ward name
    # to database ID.
    ward_ids = {}
    print("Importing {0} wards...".format(len(ward_polygons)))
    for _, ward_name, auth_name in ward_polygons:
        try:
            auth_id = authority_ids[('South West', auth_name)]
            resp = client.action(schema,
                                 ['wards', 'create'],
                                 params={'name': ward_name,
                                         'local_authority': auth_id})
            ward_ids[(auth_name, ward_name)] = resp.get('id')
        except ErrorMessage as err:
            print("Error adding ward: {0}".format(err.error))
            raise
    
    road_categories = (('PM', 'M or Class A Principal Motorway'),
                       ('PR', 'Class A Principal road in Rural area'),
                       ('PU', 'Class A Principal roadd in Urban area'),
                       ('TM', 'M or Class T Trunk Motorway'),
                       ('TR', 'Class T Trunk road in Rural area'),
                       ('TU', 'Class T trunk road in Urban area'),
                       ('BR', 'Class B road in Rural area'),
                       ('BU', 'Class B road in Urban area'),
                       ('CR', 'Class C road in Rural area'),
                       ('CU', 'Class C road in Urban area'),
                       ('UR', 'Class U road in Rural area'),
                       ('UU', 'Class U road in Urban area'))
    print("Importing {0} road categories...".format(len(road_categories)))
    # road_cat_ids will contain a mapping of category codes to database IDs.
    road_cat_ids = {}
    for cat_code, cat_desc in road_categories:
        try:
            resp = client.action(schema,
                                 ['road_categories', 'create'],
                                 params={'code': cat_code,
                                         'description': cat_desc})
            road_cat_ids[cat_code] = resp.get('id')
        except ErrorMessage as err:
            print("Error adding road category: {0}".format(err.error))
            raise        
    
    # Get a set of unique (road name, road category) pairs.
    road_cat_pairs = set([(r['Road'], r['RoadCategory']) for r in all_rows])
    print("Importing {0} roads...".format(len(road_cat_pairs)))
    # road_cat_ids will contain a mapping of (road name, category code)
    # pairs to database IDs.
    road_ids = {}
    for road_name, cat_code in road_cat_pairs:
        try:
            resp = client.action(schema,
                                 ['roads', 'create'],
                                 params={'name': road_name,
                                         'category': road_cat_ids[cat_code]})
            road_cat_ids[(road_name, cat_code)] = resp.get('id')
        except ErrorMessage as err:
            print("Error adding road: {0}".format(err.error))
            raise

    # cp_ids will contain a mapping from (CP reference, region, local authority,
    # road, road category, easting, northing, start junction, end junction) to
    # database ID. Ridiculous, but unfortunately all those values are needed to
    # uniquely identify a count point!
    cp_ids = {}
    count_points = set([(r['CP'], r['Region'], r['LocalAuthority'],
                         r['Road'], r['RoadCategory'], r['Easting'], r['Northing'],
                         r['StartJunction'], r['EndJunction'],
                         round(float(r['LinkLength_km']), 1))
                        for r in all_rows])
    print("Importing {0} count points...".format(len(count_points)))
    for cp in count_points:
        road_id = road_cat_ids[(cp[3], cp[4])]
        start_junction_id = junction_ids[cp[7]] if cp[7] in junction_ids else None
        end_junction_id = junction_ids[cp[8]] if cp[8] in junction_ids else None
        easting = int(cp[5])
        northing = int(cp[6])

        # Look up ward...
        lat, lon = OSGB36toWGS84(easting, northing)
        point = Point(lon, lat)
        auth_ward_names = [(auth_name, ward_name)
                           for poly, ward_name, auth_name in ward_polygons
                           if poly.contains(point)]
        if len(auth_ward_names) == 0:
            print("Warning: can't find ward for count point {0} (E{1} N{2}). Skipping.".format(
                cp[0], easting, northing))
            continue
        elif len(auth_ward_names) > 1:
            print("Warning: multiple wards for count point {0} (E{1} N{2}). Skipping.".format(
                cp[0], easting, northing))
            continue        

        ward_id = ward_ids[(auth_ward_names[0][0]), auth_ward_names[0][1]]
        
        try:
            resp = client.action(schema,
                                 ['count_points', 'create'],
                                 params={'reference': int(cp[0]),
                                         'ward': ward_id,
                                         'road': road_id,
                                         'easting': easting,
                                         'northing': northing,
                                         'start_junction': start_junction_id,
                                         'end_junction': end_junction_id,
                                         'link_length': cp[9]})
            key = (int(cp[0]), road_id, easting, northing, start_junction_id, end_junction_id)
            assert(key not in cp_ids)
            cp_ids[key] = resp.get('id')
        except ErrorMessage as err:
            print("Error adding count point: {0}".format(err.error))
            raise

    # Finally, import all count data.
    print("Importing {0} traffic counts...".format(len(all_rows)))
    for r in all_rows:
        road_id = road_cat_ids[(r['Road'], r['RoadCategory'])]
        start_junction_id = junction_ids[r['StartJunction']] if r['StartJunction'] in junction_ids else None
        end_junction_id = junction_ids[r['EndJunction']] if r['EndJunction'] in junction_ids else None
        est_method_id = est_method_ids[r['Estimation_method_detailed']]
        
        cp_key = (int(r['CP']), road_id, int(r['Easting']), int(r['Northing']),
                  start_junction_id, end_junction_id)

        if cp_key not in cp_ids:
            print("Warning: can't find count point {0}, skipping {1} count.".format(
                r['CP'], r['AADFYear']))
            continue
        try:
            resp = client.action(schema,
                                 ['traffic_counts', 'create'],
                                 params={'count_point': cp_ids[cp_key],
                                         'year': int(r['AADFYear']),
                                         'estimated': r['Estimation_method'] != 'Counted',
                                         'estimation_method': est_method_id,
                                         'count_cycles': int(r['PedalCycles']),
                                         'count_motorcycles': int(r['Motorcycles']),
                                         'count_cars': int(r['CarsTaxis']),
                                         'count_buses': int(r['BusesCoaches']),
                                         'count_lightgoods': int(r['LightGoodsVehicles']),
                                         'count_hgv_2ax_rigid': int(r['V2AxleRigidHGV']),
                                         'count_hgv_3ax_rigid': int(r['V3AxleRigidHGV']),
                                         'count_hgv_45ax_rigid': int(r['V4or5AxleRigidHGV']),
                                         'count_hgv_34ax_artic': int(r['V3or4AxleArticHGV']),
                                         'count_hgv_5ax_artic': int(r['V5AxleArticHGV']),
                                         'count_hgv_6plus_artic': int(r['V6orMoreAxleArticHGV'])})
        except ErrorMessage as err:
            print("Error adding road: {0}".format(err.error))
            raise        

        
    print("Import complete.")
