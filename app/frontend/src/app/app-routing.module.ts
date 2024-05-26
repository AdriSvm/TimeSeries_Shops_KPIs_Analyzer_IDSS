import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { AdministradorComponent } from './components/administrador/administrador.component';
import { TimeSeriesComponent } from './components/time-series/time-series.component';
import { mainGuard } from './guard/main.guard';
import { adminGuard } from './guard/admin.guard';

const routes: Routes = [
  { path: 'login', component: LoginComponent, pathMatch: 'full'},
  { path: "administrador", component: AdministradorComponent, pathMatch: 'full', canActivate: [mainGuard, adminGuard]},
  { path: "timeseries", component: TimeSeriesComponent, pathMatch: 'full', canActivate: [mainGuard]},
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: '**', redirectTo: '/login', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
