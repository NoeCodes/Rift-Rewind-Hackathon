import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlayerInsights } from './player-insights';

describe('PlayerInsights', () => {
  let component: PlayerInsights;
  let fixture: ComponentFixture<PlayerInsights>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlayerInsights]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PlayerInsights);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
