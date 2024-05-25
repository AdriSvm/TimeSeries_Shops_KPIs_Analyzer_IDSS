import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MainService } from 'src/app/services/main.service';

@Component({
  selector: 'app-administrador',
  templateUrl: './administrador.component.html',
  styleUrls: ['./administrador.component.css']
})
export class AdministradorComponent {

  form!:FormGroup
  error_msg = ""
  constructor(private service:MainService, private myformg: FormBuilder) {
    this.form = this.myformg.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
      type: ['user', Validators.required],
    })
   }


  send_form(data: any){
    if (this.form.invalid) {
      this.error_msg = "Por favor, rellene todos los campos"
    }
    else{
      this.service.register_user(data).subscribe((res) => {
        console.log(res);
      })
    }
 

  }

}
