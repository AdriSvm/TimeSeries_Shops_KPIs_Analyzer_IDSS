import { Component, Input, OnChanges, SimpleChanges} from '@angular/core';
import { Chart, ChartTypeRegistry } from 'chart.js/auto';
import * as Chart2 from 'chart.js';

@Component({
  selector: 'app-multi-chart-card',
  templateUrl: './multi-chart-card.component.html',
  styleUrls: ['./multi-chart-card.component.css']
})
export class MultiChartCardComponent implements OnChanges{

  @Input() data:any
  @Input() titulo: string = "";
  @Input() id: string = "";
  @Input() tipo: keyof ChartTypeRegistry = "bar";
  @Input() colores: number = 1;
  @Input() background: string = "white";
  @Input() color_text: string = "white";
  @Input() AxisColor: string = "white";
  @Input() xLabel: string = "";
  @Input() yLabel: string = "";
  @Input() legend: boolean = true ;
  @Input() fontsize: number = 20 ;
  @Input() histograma: boolean = false
  @Input() cargando: boolean = false
  @Input() clust: boolean = false
  @Input() horizontal_bar: boolean = false
  @Input() height: number = 40
  @Input() tooltip: string = ""

  chart:any
  
  colores_list:string[] = ["#EFAAC4", "#FFC4D1", "#FFE8E1", "#D4DCCD", "#339989", "#7DE2D1", "#FFFAFB", "#C7AA74", "#D55738", "#777DA7", "#94C9A9", "#C6ECAE","#C2AFF0", "#9191E9", "#457EAC", "#17B890", "#61e294", "#7bcdba", "#c9a690", "#9bc59d", "#d0fcb3"]
    //let colores = ["#FFF8E7", "#FFE2BE", "#FFC68C", "#FFA44D", "#E68A00", "#E6F2F0", "#B9E2DC", "#8CC2B5", "#558C7A", "#2E4D4F", "#FFE3F3", "#FFB6D8", "#FF8BB2", "#E85F7F", "#AD2E52", "#F3E7D3", "#E9C7B1", "#D8A28E", "#BF6E5F", "#8E382F", "#FFF4E0", "#FFD8A8", "#FFBB6E", "#F2913D", "#B86B23"]

  shuffled = this.shuffleArray(this.colores_list)
  initialized = false

  parametros:any;

  ngOnChanges(changes: SimpleChanges){
    if (this.initialized){
      if (changes["id"]){
        this.id = changes["id"].currentValue
        this.updateChart()
      }
    }
  }


  shuffleArray(array:string[]):string[] {
    var m = array.length, t, i;
 
    while (m) {    
     i = Math.floor(Math.random() * m--);
     t = array[m];
     array[m] = array[i];
     array[i] = t;
    }
 
   return array;
 }

    create_chart(id:string){      

    if (this.tipo == "doughnut" || this.tipo == "pie"){
      Chart.defaults.plugins.legend.display = true
      Chart.defaults.plugins.legend.labels.color = this.color_text
      Chart.defaults.color = this.color_text
      const canvas = document.getElementById(id) as HTMLCanvasElement;
      const ctx = canvas.getContext('2d');
      this.chart = new Chart(canvas, {
        type: this.tipo,
        data: this.data,
        options: {
        },
      });

    }
    else if (this.tipo == "line"){
      Chart.defaults.plugins.legend.display = this.legend
      Chart.defaults.color = this.color_text

      const canvas = document.getElementById(this.id) as HTMLCanvasElement;
      const ctx = canvas.getContext('2d');
      this.chart = new Chart(canvas, {
        type: this.tipo,
        data: this.data,
        options: {scales: {
          x: {
            title: {
              display: true,
              text: this.xLabel,
              font:{
                size: this.fontsize
              }
            }
          },
          y: {
            title: {
              display: true,
              text: this.yLabel,
              font:{
                size: this.fontsize
              }
            }
          }
        }
        },
      });
    }
    else if (this.tipo == "bar"){
      Chart.defaults.plugins.legend.display = this.legend
      Chart.defaults.color = this.color_text
      Chart.defaults.datasets.bar.barPercentage = 1

      const oriented_horizontal = this.horizontal_bar ? "y" : "x"

      const canvas = document.getElementById(this.id) as HTMLCanvasElement;
      const ctx = canvas.getContext('2d');
      this.chart = new Chart(canvas, {
        type: this.tipo,
        data: this.data,
        options: {
          indexAxis: oriented_horizontal,
          scales: {
            x: {
              title: {
                display: true,
                text: this.xLabel,
                font: {
                  size: this.fontsize
                }
              }
            },
            y: {
              title: {
                display: true,
                text: this.yLabel,
                font: {
                  size: this.fontsize
                }
              }
            }
          }
        }
      });

    }
    else{
      Chart.defaults.plugins.legend.display = this.legend
      Chart.defaults.color = this.color_text
      Chart.defaults.datasets.bar.barPercentage = 1

      const canvas = document.getElementById(this.id) as HTMLCanvasElement;
      const ctx = canvas.getContext('2d');
      this.chart = new Chart(canvas, {
        type: this.tipo,
        data: this.data,
        options: {
          scales: {
            x: {
              title: {
                display: true,
                text: this.xLabel,
                font: {
                  size: this.fontsize
                }
              }
            },
            y: {
              title: {
                display: true,
                text: this.yLabel,
                font: {
                  size: this.fontsize
                }
              }
            }
          }
        }
      });
    }
  }
 

  updateChart() {
    this.chart.update();
  }

  
  ngAfterViewInit(){
    this.create_chart(this.id)
    this.initialized = true
  }


}
