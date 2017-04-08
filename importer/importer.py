import coreapi
from coreapi.exceptions import ErrorMessage

import csv
from itertools import count

if __name__ == '__main__':
    # After the CSV file has been read, all_rows will contain a list
    # where each entry is name->value dictionary for a row.
    all_rows = []

    # Load and parse CSV.
    with open('Devon.csv', 'rt') as f_in:
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

    print("Import complete.")
