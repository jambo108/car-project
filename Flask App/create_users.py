from pymongo import MongoClient
import bcrypt

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.rentalDB      # select the database
users = db.users    # select the collection name

data = [
          { "name" : "Lewis Hamilton",
            "username" : "lewis",  
            "password" : b"lewis_s",
            "email" : "lewis@f1.net",
            "admin" : False
          },
          { "name" : "Jenson Button",
            "username" : "jenson",  
            "password" : b"jenson_s",
            "email" : "jenson@f1.net",
            "admin" : False
          },
          { "name" : "Jeremy Clarkson",
            "username" : "clarkson",  
            "password" : b"clarkson_s",
            "email" : "jeremy@grandtour.net",
            "admin" : False
          },        
          { "name" : "James May",
            "username" : "may",  
            "password" : b"may_s",
            "email" : "may@grandtour.net",
            "admin" : True
          },
          { "name" : "Richard Hammond",
            "username" : "hamster",  
            "password" : b"richard_s",
            "email" : "hamster@grandtour.net",
            "admin" : False
          }
       ]

for new_user in data:
      new_user["password"] = bcrypt.hashpw(new_user["password"], bcrypt.gensalt())
      users.insert_one(new_user)
