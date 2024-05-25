import { Component } from '@angular/core';
import { NavigationEnd, ROUTES, Router } from '@angular/router';
import { filter } from 'rxjs';



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'frontend';

  routes = ["login", "administrador", "time-series", "sentiment-analisis"]

  constructor(private router: Router) {}

  ngOnInit() {
    this.router.events
      .pipe(
        filter(event => event instanceof NavigationEnd)
      )
      .subscribe((event: any) => {
        if (this.isLoginPage()) {
          console.log('Estás en la página de login');
        } else {
          console.log('No estás en la página de login');
        }
      });
  }

  isLoginPage() {
    return this.router.url === '/login';
  }


}
