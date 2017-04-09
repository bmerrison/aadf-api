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
    print("Importing {0} junctions...".format(len(junc_descs)))
    # Add junctions to the database.
    for junc_desc in junc_descs:
        try:
            resp = client.action(schema,
                                 ['junctions', 'create'],
                                 params={'description': junc_desc})
        except ErrorMessage as err:
            print("Error adding junction: {0}".format(err.error))
            raise

    # Get a set of unique estimation method descriptions.
    est_method_descs = set([r["Estimation_method_detailed"]
                            for r in all_rows])
    est_method_descs.discard('')
    print("Importing {0} estimation methods...".format(len(est_method_descs)))
    # Add estimation methods to the database.
    for est_method_desc in est_method_descs:
        try:
            resp = client.action(schema,
                                 ['estimation_methods', 'create'],
                                 params={'description': est_method_desc})
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
            print("Error adding authority: {0}".format(err.error))
            raise
    print("Import complete.")
