from flask import Flask, make_response, jsonify, request
import uuid, random
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.rentalDB
cars = db.rentalDB

cars = {}

def generate_data():
    makes = ["Make 1", "Make 2", "Make 3", "Make 4", "Make 5", "Make 6", "Make 7", "Make 8", "Make 9", "Make 10"]
    
    car_dict = {}
    
    for i in range(100):
        id = str(uuid.uuid1())
        make = makes[random.randint(0, len(makes)-1)]
        model = "Car Model " + str(i)
        rating = random.randint(1, 5)
        car_dict[id] = {
            "make" : make,
            "model" : model,
            "rating" : rating,
            "reviews" : {}
        }
    return car_dict



# Handling GET, POST, PUT, and DELETE requests


@app.route("/api/v1.0/cars", methods=["GET"])
def show_all_cars():
    page_num, page_size = 1, 10
    if request.args.get("pn"):
        page_num = int(request.args.get("pn"))
    if request.args.get("ps"):
        page_size = int(request.args.get("ps"))
    page_start = page_size * (page_num - 1)
    cars_list = [ { k : v } for k, v in cars.items() ]
    data_to_return = cars_list[page_start:page_start + page_size]
    return make_response( jsonify( data_to_return ), 200 )


@app.route("/api/v1.0/cars/<string:id>", methods=["GET"])
def show_one_car(id):
    if id in cars:
        return make_response(jsonify(cars[id]), 200)
    else:
        return make_response(jsonify( { "error" : "Invalid Car ID"  }  ), 404)


@app.route("/api/v1.0/cars", methods=["POST"])
def add_car():
    if "make" in request.form and "model" in request.form and "rating" in request.form:
        next_id = str(uuid.uuid1())
        new_car = {
            "make": request.form["make"],
            "model": request.form["model"],
            "rating": request.form["rating"],
            "reviews": {}
        }
        cars[next_id]= new_car
        return make_response( jsonify( { next_id : new_car } ), 201)
    else:
        return make_response(jsonify( { "error" : "Missing Form Data"  }  ), 404)    


@app.route("/api/v1.0/cars/<string:id>", methods=["PUT"])
def edit_car(id):
    if id not in cars:
        return make_response(jsonify( { "error" : "Invalid Car ID"  }  ), 404) 
    else:
        if "make" in request.form and "model" in request.form and "rating" in request.form: 
            cars[id]["make"] = request.form["make"]
            cars[id]["model"] = request.form["model"]
            cars[id]["rating"] = request.form["rating"]      
            return make_response(jsonify( { id : cars[id] }), 200)
        else:
            return make_response(jsonify( { "error" : "Missing Form Data"  }  ), 404)


@app.route("/api/v1.0/cars/<string:id>", methods=["DELETE"])
def delete_car(id):
    if id in cars:
        del cars[id]
        return make_response(jsonify({}), 200)
    else:
        return make_response(jsonify( { "error" : "Invalid Car ID"  }  ), 404)

# Handling Reviews

@app.route("/api/v1.0/cars/<string:id>/reviews", methods=["GET"])
def fetch_all_reviews(id):
    if id not in cars:
        return make_response ( jsonify( { "error" : "Invalid car ID" } ), 404 )
    else:
        page_num, page_size = 1, 10
        if request.args.get("pn"):
            page_num = int(request.args.get("pn"))
        if request.args.get("ps"):
            page_size = int(request.args.get("ps"))
        page_start = page_size * (page_num - 1)
        reviews_list = [ { k : v } for k, v in cars[id]["reviews"].items() ]
        data_to_return = reviews_list[page_start:page_start + page_size]
        return make_response( jsonify( data_to_return ), 200 )

@app.route("/api/v1.0/cars/<string:car_id>/reviews", methods=["POST"])
def add_new_review(car_id):
    if car_id not in cars:
        return make_response ( jsonify( { "error" : "Invalid car ID" } ), 404 )
    elif "username" not in request.form or "comment" not in request.form or "stars" not in request.form:
        return make_response ( jsonify( { "error" : "Missing form data" } ), 404 )
    else:
        new_review_id = str(uuid.uuid1()) 
        new_review = { 
            "username" : request.form["username"],
            "comment" : request.form["comment"],
            "stars" : request.form["stars"]
        }
        cars[car_id]["reviews"][new_review_id] = new_review
        return make_response( jsonify( { new_review_id : new_review } ), 200 )

@app.route("/api/v1.0/cars/<string:car_id>/reviews/<string:review_id>", methods=["GET"])
def fetch_one_review(car_id, review_id):
    if car_id not in cars:
        return make_response ( jsonify( { "error" : "Invalid car ID" } ), 404 )
    elif review_id not in cars[car_id]["reviews"]:
        return make_response ( jsonify( { "error" : "Invalid review ID" } ), 404 )
    else:
        return make_response( jsonify( cars[car_id]["reviews"][review_id] ), 200)

@app.route("/api/v1.0/cars/<string:car_id>/reviews/<string:review_id>", methods=["PUT"])
def edit_review(car_id, review_id): 
    if car_id not in cars:
        return make_response ( jsonify( { "error" : "Invalid car ID" } ), 404 )
    elif review_id not in cars[car_id]["reviews"]:
        return make_response ( jsonify( { "error" : "Invalid review ID" } ), 404 )
    elif "username" not in request.form or "comment" not in request.form or "stars" not in request.form:
        return make_response ( jsonify( { "error" : "Missing form data" } ), 404 )
    else:
        cars[car_id]["reviews"][review_id]["username"] = request.form["username"]
        cars[car_id]["reviews"][review_id]["comment"] = request.form["comment"]
        cars[car_id]["reviews"][review_id]["stars"] = request.form["stars"]
        return make_response( jsonify( { review_id :  cars[car_id]["reviews"][review_id] } ), 200)            

@app.route("/api/v1.0/cars/<string:car_id>/reviews/<string:review_id>", methods=["DELETE"])
def delete_review(car_id, review_id):                
    if car_id not in cars:
        return make_response ( jsonify( { "error" : "Invalid car ID" } ), 404 )
    elif review_id not in cars[car_id]["reviews"]:
        return make_response ( jsonify( { "error" : "Invalid review ID" } ), 404 )
    else:
        del cars[car_id]["reviews"][review_id]
        return make_response( jsonify( {} ), 204)

if __name__ == "__main__":
    cars = generate_data()
    app.run(debug=True)
