import pymongo
import requests
import regex as re

class db_client():
    def __init__(self, client_url, new_db_name) -> None:
        # mongodb://localhost:27017/
        # scraperGoogleScholar
        self.client = pymongo.MongoClient(client_url)
        self.db = self.client[new_db_name]
        self.dbCollections = {}
        self.record_id = 0
        pass

    def create_collections(self, collections, schemas):
        for collection_name in collections:
            schema = schemas[collections.index(collection_name)]
            
            if collection_name not in self.db.list_collection_names():
                properties = {}
                for field in list(schema.keys()):
                    properties[field] = {
                        "bsonType": schema[field],
                        "description": "must be a " + schema[field] + " and is required"
                    }
                
                self.dbCollections[collection_name] = self.db.create_collection(collection_name, 
                    validator = {
                        "$jsonSchema": {
                            "bsonType": "object",
                            "required": list(schema.keys()),
                            "properties": properties
                        }
                    }
                )
                
        return self.dbCollections
    
    def add_data(self, pdf_name, article_name, version, abstract):
        if(self.dbCollections['articles'] == None or self.dbCollections['results'] == None):
            return -1, -1, -1
        else:
            article_collection = self.dbCollections['articles']
            results_collection = self.dbCollections['results']
            
            result_article = article_collection.insert_one({
                "id": self.record_id,
                "name": pdf_name,
            })
            
            result_results = results_collection.insert_one({
                "article_id": self.record_id,
                "name": article_name,
                "version": version,
                "abstract": abstract,
            })
            
            self.record_id+=1
            return self.record_id, result_article, result_results