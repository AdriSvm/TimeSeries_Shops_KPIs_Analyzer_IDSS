import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { AdministradorComponent } from './components/administrador/administrador.component';
import { TimeSeriesComponent } from './components/time-series/time-series.component';
import { SentimentAnalisisComponent } from './components/sentiment-analisis/sentiment-analisis.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent, pathMatch: 'full' },
  { path: "administrador", component: AdministradorComponent, pathMatch: 'full'},
  { path: "time-series", component: TimeSeriesComponent, pathMatch: 'full'},
  { path: "sentiment-analisis", component: SentimentAnalisisComponent, pathMatch: 'full'},
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: '**', redirectTo: '/login', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
