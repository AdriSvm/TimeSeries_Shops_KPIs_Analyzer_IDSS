import { Component } from '@angular/core';

@Component({
  selector: 'app-sentiment-analisis',
  templateUrl: './sentiment-analisis.component.html',
  styleUrls: ['./sentiment-analisis.component.css']
})
export class SentimentAnalisisComponent {

  data = {
    labels: ["positive", "negative", "neutral"],
    datasets : [
      {data: [300, 50, 100],
      label: 'Sentiment Analysis',
      backgroundColor: [
        'rgba(0, 255, 0, 0.2)',
        'rgba(255, 0, 0, 0.2)',
        'rgba(0, 0, 255, 0.2)'
      ],
      }
    ]
  }
}
