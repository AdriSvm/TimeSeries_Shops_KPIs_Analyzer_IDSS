import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { MainService } from '../services/main.service';

@Injectable({
  providedIn: 'root'
})
export class adminGuard implements CanActivate {

  constructor(private router: Router, private service:MainService) {}

  canActivate(): boolean {
    
    const token = this.service.getCookie('is_admin');

    if (token == 'true') {
      return true;
    } else {
      // El token no existe, el usuario no está autenticado, redirigir a la página de inicio
      this.service.logout()
      this.router.navigate(['/login']); // Cambia '/inicio' a la ruta de tu página de inicio
      return false;
    }
  }
}
