import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TimeSeriesComponent } from './time-series.component';

describe('TimeSeriesComponent', () => {
  let component: TimeSeriesComponent;
  let fixture: ComponentFixture<TimeSeriesComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [TimeSeriesComponent]
    });
    fixture = TestBed.createComponent(TimeSeriesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
