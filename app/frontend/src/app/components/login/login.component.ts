import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { MainService } from 'src/app/services/main.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {

  form!: FormGroup

  constructor(private mainservice:MainService, private myformg:FormBuilder, private routess: Router) {
    this.form = this.myformg.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    })
   }

  send_form(data: any){
    this.mainservice.login(data).subscribe((res:any) => {
      this.mainservice.setCookie('token', res['access_token'])

      //pasamos a string el valor de is_admin

      const is_admin = res['is_admin'].toString()
      console.log(is_admin)

      this.mainservice.setCookie("is_admin", is_admin)

      if (res['is_admin']){
        this.mainservice.setCookie("level", "admin")
        this.routess.navigate(['/administrador'])
      }
      else{
        this.mainservice.setCookie("level", "user")
        this.routess.navigate(['/timeseries'])
      }
      


    })
  }
}
