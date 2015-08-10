from pymongo import MongoClient

client = MongoClient()
db = client.test_database
#collection = db.test_collection #this is not used. MongoDB does a lazy creation of collections (does not actually create the collection until something is inserted into the collection)
post = {"author": "Sam", "text": "My second blog post!"}
posts = db.posts
post_id = posts.insert_one(post).inserted_id
#post_id = posts.update({"text":"My first blog post!"},post)

db.collection_names(include_system_collections=False) #this lists all the collections created


posts.find_one({"_id": post_id}) #finds the document with id post_id


















