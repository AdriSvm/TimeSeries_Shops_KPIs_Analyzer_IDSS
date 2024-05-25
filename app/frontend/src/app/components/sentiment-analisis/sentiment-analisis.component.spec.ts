import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SentimentAnalisisComponent } from './sentiment-analisis.component';

describe('SentimentAnalisisComponent', () => {
  let component: SentimentAnalisisComponent;
  let fixture: ComponentFixture<SentimentAnalisisComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SentimentAnalisisComponent]
    });
    fixture = TestBed.createComponent(SentimentAnalisisComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
