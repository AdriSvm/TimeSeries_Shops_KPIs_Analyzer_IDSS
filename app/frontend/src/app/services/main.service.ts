import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root'
})
export class MainService {

  constructor(private http: HttpClient, private cookie: CookieService) { }

  login(data: any){
    return this.http.post('http://localhost:8000/login', data)
  }

  setCookie(key: string, value: string){
    this.cookie.set(key, value)
  }

  getCookie(key: string){
    return this.cookie.get(key)
  }

  register_user(data: any){
    return this.http.post('http://localhost:8000/register', data)
  }

}
