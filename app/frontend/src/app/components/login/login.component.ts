import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MainService } from 'src/app/services/main.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {

  form!: FormGroup

  constructor(private mainservice:MainService, private myformg:FormBuilder) {
    this.form = this.myformg.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    })
   }

   


  send_form(data: any){
    /*this.mainservice.login(data).subscribe((res) => {
      console.log(res);
    })*/
    if (data.username == "admin" && data.password == "admin"){
      console.log("Login correcto")
      this.mainservice.setCookie("level", "admin")
    }
    else{
      console.log("Login incorrecto")
      this.mainservice.setCookie("level", "user")
    }

  }
}
