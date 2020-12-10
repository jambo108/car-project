import { Component } from '@angular/core';
import { WebService } from './web.service';
import { FormBuilder, Validators } from '@angular/forms';
import { AuthService } from './auth.service'
import { NgxPaginationModule } from 'ngx-pagination';

@Component({
  selector: 'cars',
  templateUrl: './cars.component.html',
  styleUrls: ['./cars.component.css']
})
export class CarsComponent {

  carForm;

  constructor(public webService: WebService,
    public formBuilder: FormBuilder,
    public authService: AuthService) {

    this.carForm = formBuilder.group(
      {
        make: ['', Validators.required],
        model: ['', Validators.required],
        year: 2020,
        type: 'Hatchback',
        engine: 2.0,
        fuel: 'Petrol',
        doors: 3,
        mpg: 30,
        image_file: 'https://tinyurl.com/y2mcaakc'
      }
    )
  }


  ngOnInit() {
    if (sessionStorage.page) {
      this.page = sessionStorage.page;
    }
    this.webService.getCars(this.page);
  }

  onSubmit() {
    console.log(this.carForm.value);
    this.webService.postCar(this.carForm.value);
    this.carForm.reset();
  }

  isInvalidCar(control) {
    return this.carForm.controls[control].invalid && this.carForm.controls[control].touched;
  }

  isUntouchedCar() {
    return this.carForm.controls.make.pristine || this.carForm.controls.model.pristine || this.carForm.controls.model.pristine;
  }

  isIncompleteCar() {
    return this.isInvalidCar('make') ||  this.isUntouchedCar();
  }

  nextPage() {
    this.page = Number(this.page) + 1;
    sessionStorage.page = Number(this.page);
    this.webService.getCars(this.page);
  }

  previousPage() {
    if (this.page > 1) {
      this.page = Number(this.page) - 1;
      sessionStorage.page = Number(this.page);
      this.webService.getCars(this.page);
    }
  }

  car_list;
  page = 1;

}
