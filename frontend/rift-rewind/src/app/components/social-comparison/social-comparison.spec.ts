import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SocialComparison } from './social-comparison';

describe('SocialComparison', () => {
  let component: SocialComparison;
  let fixture: ComponentFixture<SocialComparison>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SocialComparison]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SocialComparison);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
