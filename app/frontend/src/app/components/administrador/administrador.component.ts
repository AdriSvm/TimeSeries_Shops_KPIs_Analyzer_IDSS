import { AfterViewInit, Component, ViewChild } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MainService } from 'src/app/services/main.service';

@Component({
  selector: 'app-administrador',
  templateUrl: './administrador.component.html',
  styleUrls: ['./administrador.component.css']
})
export class AdministradorComponent  implements AfterViewInit{

  form!:FormGroup
  error_msg = ""
  error_sccss = ""
  dataSource: any
  displayedColumns: string[] = ['fldIdUsuario', 'fldIdAlmacen', 'fldIdClaveAcceso', 'fldIdNivelAcceso', 'eliminar'];

  users: any = []

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(private service:MainService, private myformg: FormBuilder) {
    this.form = this.myformg.group({
      username: ['', [Validators.required, Validators.maxLength(6)]],
      password: ['', Validators.required],
      is_admin: [false, Validators.required],
      idalmacen: [0, [Validators.required, Validators.pattern("^[0-9]*$")]]
    })
   }

  ngAfterViewInit() {
    this.get_users()
  }

   applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

  t(){
    return this.form.controls
  }

  transform_level(level: string){
    if (level == "0000"){
      return "User"
    }
    else{
      return "Admin"
    }
  }


  send_form(data: any){
    this.error_msg = ""
    this.error_sccss = ""
    if (this.form.invalid) {

      const controls = this.t()

      if (controls["username"].errors?.["required"]){
        this.error_msg = "Por favor, rellene el campo de usuario"
      }
      else if (controls["username"].errors?.["maxlength"]){
        this.error_msg = "El usuario no puede tener más de 6 caracteres"
      }
      else if (controls["password"].errors?.["required"]){
        this.error_msg = "Por favor, rellene el campo de contraseña"
      }
      else if (controls["is_admin"].errors?.["required"]){
        this.error_msg = "Por favor, seleccione un tipo de usuario"
      }
      else if (controls["idalmacen"].errors?.["required"]){
        this.error_msg = "Por favor, rellene el campo de id de almacen"
      }
      else if (controls["idalmacen"].errors?.["pattern"]){
        this.error_msg = "El id de almacen solo puede contener números"
      }
      else{
        this.error_msg = "Por favor, rellene todos los campos"
      }

    }
    else{

      var data2 = data
      data2["idalmacen"] = this.rellenar_con_0(data["idalmacen"]) 


      this.service.register_user(data2).subscribe((res) => {
        this.error_sccss = "Usuario registrado correctamente"
        this.form.reset()
        this.error_msg = ""
        this.get_users()
      })
    }
  }

  get_users(){
    this.service.get_users().subscribe((res:any) => {
      this.users = res["users"]

      for (let index = 0; index < this.users.length; index++) {
        const element = this.users[index];
        element["eliminar"] = element["fldIdUsuario"]
        this.users[index] = element
      }

      this.dataSource = this.users
      this.dataSource.paginator = this.paginator;
      this.dataSource.sort = this.sort;

    })
  }

  delete_user(id: number){
    var data = {username: id}
    this.service.delete_user(data).subscribe((res) => {
      this.get_users()
      this.error_sccss = "Usuario eliminado correctamente"
    }, (error) => {
      this.error_msg = "No puedes eliminarte a ti mismo"
  })
  }

  rellenar_con_0(id: number){
    return id.toString().padStart(8, "0")
  }

}
