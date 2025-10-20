import { ComponentFixture, TestBed } from '@angular/core/testing';

import { YearRecap } from './year-recap';

describe('YearRecap', () => {
  let component: YearRecap;
  let fixture: ComponentFixture<YearRecap>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [YearRecap]
    })
    .compileComponents();

    fixture = TestBed.createComponent(YearRecap);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
