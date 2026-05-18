import bibtexparser
import json
import os
import shutil
import urllib.request
import yaml

json_filename = "_data/publications.json"
yml_filename = "_data/publications.yml"
bib_filename = "_data/publications.bib"

bib_file_url = "https://publications.imp.fu-berlin.de/cgi/exportview/divisions/group=5Falgbioinf/BibTeX/group=5Falgbioinf.bib"
json_file_url = "https://publications.imp.fu-berlin.de/cgi/exportview/divisions/group=5Falgbioinf/JSON/group=5Falgbioinf.js"

def download_file(url, destination):
    with urllib.request.urlopen(url) as response, open(destination, "wb") as out_file:
        shutil.copyfileobj(response, out_file)


# download publication files
download_file(bib_file_url, bib_filename)
download_file(json_file_url, json_filename)

# parse the bibtex file
with open(bib_filename) as bib_file:
    bib = bibtexparser.load(bib_file)

# parse the json file
with open(json_filename) as json_file:
    js = json.load(json_file)

for entry in js:
    # replace the keys
    entry["key"] = "fu_mi_publications" + str(entry["eprintid"])
    # extract the corresponding bibtex entry
    temp_entry = bib.entries_dict[entry["key"]]
    # create new temporary database
    temp_db = bibtexparser.bibdatabase.BibDatabase()
    # Insert temporary entry into temporary Database
    temp_db.entries = [temp_entry]
    # insert bibtex string into the json entry
    entry["bibtex"] = bibtexparser.dumps(temp_db)
    del temp_db, temp_entry

# overwrite yaml with sorted entries
with open( yml_filename, 'w') as out_file:
    documents = yaml.dump(sorted(js, key=lambda x: x['key']), out_file, explicit_start=True)

# remove json and bib files
os.remove(json_filename)
os.remove(bib_filename)
