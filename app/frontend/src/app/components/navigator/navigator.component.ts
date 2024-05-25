import { Component } from '@angular/core';
import { MainService } from 'src/app/services/main.service';

@Component({
  selector: 'app-navigator',
  templateUrl: './navigator.component.html',
  styleUrls: ['./navigator.component.css']
})
export class NavigatorComponent {

  constructor(private service: MainService) { }

  routes = ["login", "administrador", "time-series", "sentiment-analisis"]
  icons = ["bi bi-box-arrow-in-right", "bi bi-person", "bi bi-bar-chart", "bi bi-chat-right-text"]

  ngAfterViewInit() {
    var val = this.service.getCookie("level")
    if (val == "admin") {
      this.routes = ["administrador", "time-series", "sentiment-analisis"]
      this.icons = ["bi bi-person", "bi bi-bar-chart", "bi bi-chat-right-text"]
    }
    else {
      this.routes = ["time-series", "sentiment-analisis"]
      this.icons = ["bi bi-bar-chart", "bi bi-chat-right-text"]
    }

  }
}
