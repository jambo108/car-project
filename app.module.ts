import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router'

import { AppComponent } from './app.component';
import { CarsComponent} from './cars.component';
import { WebService } from './web.service';
import { HttpClientModule } from '@angular/common/http'; 
import { HomeComponent } from './home.component'
import { CarComponent} from './car.component';
import { FormsModule, ReactiveFormsModule} from '@angular/forms';
import { AuthService } from './auth.service';
import { NavComponent } from './nav.component';
import { EditCarComponent } from './editcar.component';


var routes = [
  {
    path: '', 
    component: HomeComponent
  },
  {
    path: 'cars',
    component: CarsComponent
  },
  {
    path: 'cars/:id',
    component: CarComponent
  }
  
];

@NgModule({
  declarations: [
    AppComponent, CarsComponent, HomeComponent, CarComponent, NavComponent, EditCarComponent
  ],
  imports: [
    BrowserModule, HttpClientModule, RouterModule.forRoot(routes), FormsModule, ReactiveFormsModule
  ],
  providers: [WebService, AuthService],
  bootstrap: [AppComponent]
})
export class AppModule { }
