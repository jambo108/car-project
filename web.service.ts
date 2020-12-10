import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable()
export class WebService{

    private car_private_list;
    carsSubject = new Subject();
    car_list = this.carsSubject.asObservable();

    private car_private;
    carSubject = new Subject();
    car = this.carSubject.asObservable();

    private reviews_private_list;
    reviewsSubject = new Subject();
    reviews_list = this.reviewsSubject.asObservable();

    carID;
    reviewID;

    constructor(private http: HttpClient){}
        
        getCars(page){
            return this.http.get('http://localhost:5000/api/v1.0/cars?pn=' + page)
                .subscribe(response => {
                    this.car_private_list = response;
                    this.carsSubject.next(this.car_private_list);
                })
        }


        getCar(id){
            return this.http.get('http://localhost:5000/api/v1.0/cars/' + id)
            .subscribe(response => {
                this.car_private = [response];
                this.carSubject.next(this.car_private);
                this.carID = id;
            })
        }

        getReviews(id){
            return this.http.get('http://localhost:5000/api/v1.0/cars/' + id + '/reviews')
                .subscribe(response => {
                    this.reviews_private_list = response;
                    this.reviewsSubject.next(this.reviews_private_list);
                })
        }

        postReview(review){
            let postData = new FormData();
            postData.append("username", review.name);
            postData.append("text", review.review);
            postData.append("stars", review.stars);
            
            let today = new Date();
            let todayDate = today.getFullYear() + "-" + today.getMonth() + "-" + today.getDate();
            postData.append("date", todayDate);

            this.http.post('http://localhost:5000/api/v1.0/cars/' + this.carID + '/reviews', postData).subscribe(
                response => {
                    this.getReviews(this.carID);
                }
            );
            
        }

        deleteReview(){
            this.http.delete('http://localhost:5000/api/v1.0/cars/' + this.carID + '/reviews/' + this.reviewID).subscribe(
                response => {
                    this.getReviews(this.carID);
                }
            );
        }

        postCar(car){
            let postData = new FormData();
            postData.append("make", car.make);
            postData.append("model", car.model);
            postData.append("year", car.year);
            postData.append("type", car.type);
            postData.append("fuel", car.fuel);
            postData.append("doors", car.doors);
            postData.append("engine", car.engine);
            postData.append("mpg", car.mpg);
            postData.append("image_file", car.image_file);

            this.http.post('http://localhost:5000/api/v1.0/cars', postData).subscribe(
                response => {
                    this.getCars;
                }
            );
        }

        deleteCar(){
            this.http.delete('http://localhost:5000/api/v1.0/cars/' + this.carID).subscribe(
                response=> {
                    this.getCars;
                }
            )
        }
    }
