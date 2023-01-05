import pymongo
import requests
import regex as re

class db_client():
    def __init__(self, client_url, new_db_name) -> None:
        # mongodb://localhost:27017/
        # scraperGoogleScholar
        self.client = pymongo.MongoClient(client_url)
        self.db = self.client[new_db_name]
        self.dbCollectionA = None
        self.dbCollectionB = None
        self.record_id = 0
        pass

    def create_collection_A(self, collection_name, schema_fields):
        properties = {}
        for field in list(schema_fields.keys()):
            properties[field] = {
                "bsonType": schema_fields[field],
                "description": "must be a " + schema_fields[field] + " and is required"
            }
        
        self.dbCollectionA = self.db.create_collection(collection_name, 
            validator = {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": list(schema_fields.keys()),
                    "properties": properties
                }
            }
        )
        return self.dbCollectionA 
    
    def create_collection_B(self, collection_name, schema_fields):
        properties = {}
        for field in list(schema_fields.keys()):
            properties[field] = {
                "bsonType": schema_fields[field],
                "description": "must be a " + schema_fields[field] + " and is required"
            }
        
        self.dbCollectionB = self.db.create_collection(collection_name, 
            validator = {
                "$jsonSchema": {
                    "bsonType": "object",
                    "required": list(schema_fields.keys()),
                    "properties": properties
                }
            }
        )
        return self.dbCollectionB 
        

    def add_data(self, pdf_name, article_name, version, abstract):
        if(self.dbCollectionA == None or self.dbCollectionB == None):
            return '[STATUS]: One of the collections is not selected.'
        else:
            article_collection = self.dbCollectionA
            results_collection = self.dbCollectionB
            
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