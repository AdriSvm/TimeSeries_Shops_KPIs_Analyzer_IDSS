import { AfterViewInit, Component } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { MainService } from 'src/app/services/main.service';

@Component({
  selector: 'app-time-series',
  templateUrl: './time-series.component.html',
  styleUrls: ['./time-series.component.css']
})
export class TimeSeriesComponent{

  
  data:any
  tabla:any 
  first_row:any 
  registers_plot:any
  form!: FormGroup
  clusters_colors:any

  minDate = new Date(2021, 0, 1);
  maxDate = new Date(2023, 11, 31);

  constructor(private mainservice:MainService, private formgroupb: FormBuilder) { 
    this.form = this.formgroupb.group({
      start: new FormControl<Date | null>(null),
      end: new FormControl<Date | null>(null),
    })
  }

  send_form(data: any){
    this.mainservice.send_data(data).subscribe((res:any) => {
      this.data = res["plot"]
      this.tabla = res["table"]
      this.first_row = res["first_row"]
      this.registers_plot = res["registers_plot"]
      this.clusters_colors = res["cluster_colors"]

    })
  }

}
