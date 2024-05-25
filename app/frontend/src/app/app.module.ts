import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './components/login/login.component';
import { AdministradorComponent } from './components/administrador/administrador.component';
import { TimeSeriesComponent } from './components/time-series/time-series.component';
import { SentimentAnalisisComponent } from './components/sentiment-analisis/sentiment-analisis.component';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { MainService } from './services/main.service';
import { MultiChartCardComponent } from './components/multi-chart-card/multi-chart-card.component';
import { NavigatorComponent } from './components/navigator/navigator.component';
import { CookieService } from 'ngx-cookie-service';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    AdministradorComponent,
    TimeSeriesComponent,
    SentimentAnalisisComponent,
    MultiChartCardComponent,
    NavigatorComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  providers: [
    MainService,
    CookieService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
