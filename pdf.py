import pymongo
import requests
import regex as re


class db_client():
    def __init__(self, client_url, new_db_name) -> None:
        # mongodb://localhost:27017/
        # scraperGoogleScholar
        self.client = pymongo.MongoClient(client_url)
        self.db = self.client[new_db_name]
        self.dbCollection = None
        pass

    def create_collection(self, collection_name, schema_fields):
        # schema_fields = { 'title': 'string', 'pdf_name': 'string', 'URI', 'string'}
        properties = {}
        for field in list(schema_fields.keys()):
            properties[field] = {
                "bsonType": schema_fields[field],
                "description": "must be a " + schema_fields[field] + " and is required"
            }
        
        self.dbCollection = self.db.create_collection(collection_name, 
            validator = {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": list(schema_fields.keys()),
                    "properties": properties
                }
            }
        )
        
        return self.dbCollection 
        

    def add_data(self, title, pdf_filename, uri):
        if(self.dbCollection == None):
            return 'No Collection Selected.'
        else:
            results = self.dbCollection
            result = results.insert_one({
                "title": title,
                "pdf_name": pdf_filename,
                "URI": uri
            })
            return result

title = 'Are we there yet? Data saturation in qualitative research'
pdf_url = 'https://scholarworks.waldenu.edu/cgi/viewcontent.cgi?article=1466&context=facpubs'
pdf_filename = re.sub(r'[^\w\s]' , '-', title) + '.pdf'
chunk_size = 2000

r = requests.get(pdf_url, stream=True)
with open(pdf_filename, 'wb') as f:
    for chunk in r.iter_content(chunk_size):
        f.write(chunk)

dbc = db_client('mongodb://localhost:27017/', 'scraperGoogleScholar')
dbc.create_collection('results', {'title': 'string', 'pdf_name': 'string', 'URI': 'string'})
result = dbc.add_data(title, pdf_filename, 'okay')
print(result.inserted_id)
print(dbc.client.list_database_names())
