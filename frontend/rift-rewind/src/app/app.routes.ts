import { Routes } from '@angular/router';
import { Dashboard } from './components/dashboard/dashboard';
import { YearRecap } from './components/year-recap/year-recap';
import { PlayerInsights } from './components/player-insights/player-insights';
import { ChampionStats } from './components/champion-stats/champion-stats';
import { SocialComparison } from './components/social-comparison/social-comparison';

export const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: Dashboard },
  { path: 'year-recap', component: YearRecap },
  { path: 'insights', component: PlayerInsights },
  { path: 'champions', component: ChampionStats },
  { path: 'social', component: SocialComparison }
];
