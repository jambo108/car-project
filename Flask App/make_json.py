import random, json

cars = {}

def generate_data():
    makes = ["Make 1", "Make 2", "Make 3", "Make 4", "Make 5", "Make 6", "Make 7", "Make 8", "Make 9", "Make 10"]
    
    car_list = []
    
    for i in range(100):
        make = makes[random.randint(0, len(makes)-1)]
        model = "Car Model " + str(i)
        rating = random.randint(1, 5)
        car_list.append( {
            "make" : make,
            "model" : model,
            "rating" : rating,
            "reviews" : []
        })
    return car_list

cars = generate_data()
fout = open("data.json", "w")
fout.write(json.dumps(cars))
fout.close()