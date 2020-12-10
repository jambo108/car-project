import { Component, Input } from '@angular/core';
import { WebService } from './web.service';
import { ActivatedRoute } from '@angular/router';
import { FormBuilder, Validators  } from '@angular/forms';
import { AuthService } from './auth.service'

@Component({
  selector: 'car',
  templateUrl: './car.component.html',
  styleUrls: ['./car.component.css']
})
export class CarComponent {

  @Input() carID
  reviewForm;
  
    constructor(public webService: WebService,
                private route: ActivatedRoute,
                public formBuilder : FormBuilder,
                public authService: AuthService){
      
      this.reviewForm = formBuilder.group(
        {
          name: ['', Validators.required],
          review: ['', Validators.required],
          stars: 5
        }
      )            
    }
      
  ngOnInit(){
      this.webService.getCar(this.route.snapshot.params.id);
      this.webService.getReviews(this.route.snapshot.params.id);
      
  }

  onSubmit(){
    console.log(this.reviewForm.value);
    this.webService.postReview(this.reviewForm.value);
    this.reviewForm.reset();
  }

  onDeleteCar(id){
    this.webService.deleteCar()
  }

  onDelete(id){
    this.webService.deleteReview()
  }

  isInvalid(control){
    return this.reviewForm.controls[control].invalid && 
           this.reviewForm.controls[control].touched;
  }

  isUntouched(){
    return this.reviewForm.controls.name.pristine || 
           this.reviewForm.controls.review.pristine;
  }

  isIncomplete(){
    return this.isInvalid('name') || this.isInvalid('review') || this.isUntouched();
  }

    car;

}
