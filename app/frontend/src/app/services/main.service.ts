import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';

@Injectable({
  providedIn: 'root'
})
export class MainService {

  constructor(private http: HttpClient, private cookie: CookieService) { }

  // ---------------------------------- Login ----------------------------------

  login(data: any){
    return this.http.post('login/', data)
  }

  // ---------------------------------- Cookies ----------------------------------

  setCookie(key: string, value: string){
    this.cookie.set(key, value)
  }

  getCookie(key: string){
    return this.cookie.get(key)
  }

  // ---------------------------------- Administrator ----------------------------------

  register_user(data: any){
    const token = this.cookie.get("token")

    const headers = {
      Authorization: `Bearer ${token}`
    }

    return this.http.post('register/', data, {headers:headers})
  }

  get_users(){
    const token = this.cookie.get("token")

    const headers = {
      Authorization: `Bearer ${token}`
    }
    return this.http.get('get_users/', {headers:headers})
  }

  delete_user(data: any){
    const token = this.cookie.get("token")

    const headers = {
      Authorization: `Bearer ${token}`
    }

    return this.http.post('delete_user/', data, {headers:headers})
  }

  // ---------------------------------- Time Series ----------------------------------

  send_data(data: any){
    const token = this.cookie.get("token")

    const headers = {
      Authorization: `Bearer ${token}`
    }

    return this.http.post('get_info/', data, {headers:headers})
  }

  // ---------------------------------- Sentiment analisis ----------------------------------

  get_sentiment(){

    const token = this.cookie.get("token")

    const headers = {
      Authorization: `Bearer ${token}`
    }

    return this.http.get('sentiment/', {headers:headers})
  }

  // ---------------------------------- Logout ----------------------------------

  logout(){
    this.cookie.deleteAll()
    localStorage.clear()
  }



}
