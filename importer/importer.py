import coreapi
from coreapi.exceptions import ErrorMessage

import csv, sys
from itertools import count

if __name__ == '__main__':
    csv_path = sys.argv[1]
    
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

      
    client = coreapi.Client()
    schema = client.get('http://localhost:8000/schema')
    print(schema)

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
    region_auth_pairs = set([(r['Region'], r['LocalAuthority']) for r in all_rows])
    print("Importing {0} local authorities...".format(len(region_auth_pairs)))
    # region_auth_ids will contain a mapping of (region,auth) name
    # pairs to database IDs.
    authority_ids = {}
    for region_name, authority_name in region_auth_pairs:
        try:
            resp = client.action(schema,
                                 ['local_authorities', 'create'],
                                 params={'name': authority_name,
                                         'region': region_ids[region_name]})
            authority_ids[(region_name, authority_name)] = resp.get('id')
        except ErrorMessage as err:
            print("Error adding local authority: {0}".format(err.error))
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
        auth_id = authority_ids[(cp[1], cp[2])]
        road_id = road_cat_ids[(cp[3], cp[4])]
        start_junction_id = junction_ids[cp[7]] if cp[7] in junction_ids else None
        end_junction_id = junction_ids[cp[8]] if cp[8] in junction_ids else None
        try:
            resp = client.action(schema,
                                 ['count_points', 'create'],
                                 params={'reference': int(cp[0]),
                                         'local_authority': auth_id,
                                         'road': road_id,
                                         'easting': int(cp[5]),
                                         'northing': int(cp[6]),
                                         'start_junction': start_junction_id,
                                         'end_junction': end_junction_id,
                                         'link_length': cp[9]})
            key = (int(cp[0]), auth_id, road_id, int(cp[5]), int(cp[6]), start_junction_id, end_junction_id)
            assert(key not in cp_ids)
            cp_ids[key] = resp.get('id')
        except ErrorMessage as err:
            print("Error adding count point: {0}".format(err.error))
            raise

    # Finally, import all count data.
    print("Importing {0} traffic counts...".format(len(all_rows)))
    for r in all_rows:
        auth_id = authority_ids[(r['Region'], r['LocalAuthority'])]
        road_id = road_cat_ids[(r['Road'], r['RoadCategory'])]
        start_junction_id = junction_ids[r['StartJunction']] if r['StartJunction'] in junction_ids else None
        end_junction_id = junction_ids[r['EndJunction']] if r['EndJunction'] in junction_ids else None
        est_method_id = est_method_ids[r['Estimation_method_detailed']]
        
        cp_key = (int(r['CP']), auth_id, road_id, int(r['Easting']), int(r['Northing']),
                  start_junction_id, end_junction_id)
        
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
