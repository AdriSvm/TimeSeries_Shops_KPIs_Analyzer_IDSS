import { Component } from '@angular/core';
import { MainService } from 'src/app/services/main.service';

@Component({
  selector: 'app-navigator',
  templateUrl: './navigator.component.html',
  styleUrls: ['./navigator.component.css']
})
export class NavigatorComponent {

  constructor(private service: MainService) { }

  routes = ["login", "administrador", "timeseries" ]
  icons = ["bi bi-box-arrow-in-right", "bi bi-person", "bi bi-bar-chart"]

  ngAfterViewInit() {
    var val = this.service.getCookie("level")
    if (val == "admin") {
      this.routes = ["administrador", "timeseries"]
      this.icons = ["bi bi-person", "bi bi-bar-chart"]
    }
    else {
      this.routes = ["timeseries"]
      this.icons = ["bi bi-bar-chart"]
    }

  }
}
