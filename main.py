import csv
for r in csv.DictReader(open('data/processed/failed_runs.csv')):
    if r['candidate']=='True' and r['faap_trigger']!='spec_neglect':
        print(r['run_id'], '|', r['faap_trigger'], '|', r['faap_category'])
        