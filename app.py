from flask import Flask, jsonify, make_response, request
import uuid, random

app = Flask(__name__)

businesses =  {}

def generate_dummy_data():
    towns = ['Coleraine', 'Banbridge', 'Belfast', 'Lisburn',
    'Ballymena', 'Derry', 'Newry', 'Enniskillen', 'Omagh', 'Ballymoney']

    business_dict = {}

    for i in range(100):
        id = str(uuid.uuid1())
        name = 'Biz ' + str(i)
        town = towns[random.randint(0, len(towns)-1)]
        rating = random.randint(1, 5)
        business_dict[id] = {
            "name" : name,
            "town" : town,
            "rating" : rating,
            "reviews" : {}
        }
    return business_dict

@app.route("/api/v1.0/businesses", methods=["GET"])
def show_all_businesses():
    page_num, page_size = 1, 10
    if request.args.get("pn"):
        page_num = int(request.args.get("pn"))
    if request.args.get("ps"):
        page_size = int(request.args.get("ps"))
    page_start = page_size * (page_num - 1)
    businesses_list = [ { k : v } for k, v in businesses.items() ]
    data_to_return = businesses_list[page_start:page_start + page_size]
    return make_response( jsonify( data_to_return ), 200 )

@app.route("/api/v1.0/businesses/<string:id>", \
           methods=["GET"])
def show_one_business(id):
    if id in businesses:
        return make_response( jsonify(  businesses[id] ), 200 )
    else:
        return make_response ( jsonify( { "error" : "Invalid business ID" } ), 404 )

@app.route("/api/v1.0/businesses", methods=["POST"])
def add_business():
    if "name" in request.form and "town" in request.form and "rating" in request.form:
        next_id = str(uuid.uuid1())
        new_business = { "name" : request.form["name"],
                        "town" : request.form["town"],
                        "rating" : request.form["rating"],
                        "reviews" : {} 
                        }
        businesses[next_id] = new_business
        return make_response( jsonify( { next_id : new_business } ), 201 )
    else:
        return make_response ( jsonify( { "error" : "Missing form data" } ), 404 )

@app.route("/api/v1.0/businesses/<string:id>", methods=["PUT"])
def edit_business(id):
    if id not in businesses:
        return make_response ( jsonify( { "error" : "Invalid business ID" } ), 404 )
    else:
        if "name" in request.form and "town" in request.form and "rating" in request.form:
            businesses[id]["name"] = request.form["name"]
            businesses[id]["town"] = request.form["town"]
            businesses[id]["rating"] = request.form["rating"]
            return make_response( jsonify( { id: businesses[id] } ), 200 )
        else:
            return make_response ( jsonify( { "error" : "Missing form data" } ), 404 )
 
@app.route("/api/v1.0/businesses/<string:id>", methods=["DELETE"])
def delete_business(id):
    if id in businesses:
        del businesses[id]
        return make_response( jsonify( {} ), 204)
    else:
        return make_response ( jsonify( { "error" : "Invalid business ID" } ), 404 )
    

@app.route("/api/v1.0/businesses/<string:id>/reviews", methods=["GET"])
def fetch_all_reviews(id):
    if id not in businesses:
        return make_response ( jsonify( { "error" : "Invalid business ID" } ), 404 )
    else:
        page_num, page_size = 1, 10
        if request.args.get("pn"):
            page_num = int(request.args.get("pn"))
        if request.args.get("ps"):
            page_size = int(request.args.get("ps"))
        page_start = page_size * (page_num - 1)
        reviews_list = [ { k : v } for k, v in businesses[id]["reviews"].items() ]
        data_to_return = reviews_list[page_start:page_start + page_size]
        return make_response( jsonify( data_to_return ), 200 )

@app.route("/api/v1.0/businesses/<string:business_id>/reviews", methods=["POST"])
def add_new_review(business_id):
    if business_id not in businesses:
        return make_response ( jsonify( { "error" : "Invalid business ID" } ), 404 )
    elif "username" not in request.form or "comment" not in request.form or "stars" not in request.form:
        return make_response ( jsonify( { "error" : "Missing form data" } ), 404 )
    else:
        new_review_id = str(uuid.uuid1()) 
        new_review = { 
            "username" : request.form["username"],
            "comment" : request.form["comment"],
            "stars" : request.form["stars"]
        }
        businesses[business_id]["reviews"][new_review_id] = new_review
        return make_response( jsonify( { new_review_id : new_review } ), 200 )

@app.route("/api/v1.0/businesses/<string:business_id>/reviews/<string:review_id>", methods=["GET"])
def fetch_one_review(business_id, review_id):
    if business_id not in businesses:
        return make_response ( jsonify( { "error" : "Invalid business ID" } ), 404 )
    elif review_id not in businesses[business_id]["reviews"]:
        return make_response ( jsonify( { "error" : "Invalid review ID" } ), 404 )
    else:
        return make_response( jsonify( businesses[business_id]["reviews"][review_id] ), 200)

@app.route("/api/v1.0/businesses/<string:business_id>/reviews/<string:review_id>", methods=["PUT"])
def edit_review(business_id, review_id): 
    if business_id not in businesses:
        return make_response ( jsonify( { "error" : "Invalid business ID" } ), 404 )
    elif review_id not in businesses[business_id]["reviews"]:
        return make_response ( jsonify( { "error" : "Invalid review ID" } ), 404 )
    elif "username" not in request.form or "comment" not in request.form or "stars" not in request.form:
        return make_response ( jsonify( { "error" : "Missing form data" } ), 404 )
    else:
        businesses[business_id]["reviews"][review_id]["username"] = request.form["username"]
        businesses[business_id]["reviews"][review_id]["comment"] = request.form["comment"]
        businesses[business_id]["reviews"][review_id]["stars"] = request.form["stars"]
        return make_response( jsonify( { review_id :  businesses[business_id]["reviews"][review_id] } ), 200)            

@app.route("/api/v1.0/businesses/<string:business_id>/reviews/<string:review_id>", methods=["DELETE"])
def delete_review(business_id, review_id):                
    if business_id not in businesses:
        return make_response ( jsonify( { "error" : "Invalid business ID" } ), 404 )
    elif review_id not in businesses[business_id]["reviews"]:
        return make_response ( jsonify( { "error" : "Invalid review ID" } ), 404 )
    else:
        del businesses[business_id]["reviews"][review_id]
        return make_response( jsonify( {} ), 204)

if __name__ == "__main__":
    businesses = generate_dummy_data()
    app.run(debug=True)
