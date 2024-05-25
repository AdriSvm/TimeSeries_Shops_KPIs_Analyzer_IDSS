import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MultiChartCardComponent } from './multi-chart-card.component';

describe('MultiChartCardComponent', () => {
  let component: MultiChartCardComponent;
  let fixture: ComponentFixture<MultiChartCardComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [MultiChartCardComponent]
    });
    fixture = TestBed.createComponent(MultiChartCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
