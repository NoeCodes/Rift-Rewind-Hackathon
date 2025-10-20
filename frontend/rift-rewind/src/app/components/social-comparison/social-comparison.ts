import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-social-comparison',
  imports: [CommonModule],
  templateUrl: './social-comparison.html',
  styleUrl: './social-comparison.scss'
})
export class SocialComparison {
  friends = [
    { name: 'You', rank: 'Gold II', winRate: 54.3, kda: 3.2, games: 1247, topChamp: 'Ahri', isYou: true },
    { name: 'FriendOne', rank: 'Platinum IV', winRate: 52.1, kda: 2.9, games: 892, topChamp: 'Lee Sin', isYou: false },
    { name: 'FriendTwo', rank: 'Gold I', winRate: 56.8, kda: 3.5, games: 743, topChamp: 'Thresh', isYou: false },
    { name: 'FriendThree', rank: 'Silver I', winRate: 48.9, kda: 2.4, games: 654, topChamp: 'Garen', isYou: false },
    { name: 'FriendFour', rank: 'Gold III', winRate: 53.2, kda: 3.0, games: 567, topChamp: 'Lux', isYou: false }
  ];

  playstyleCompatibility = [
    { name: 'FriendTwo', compatibility: 94, reason: 'Both excel at team fighting and vision control', style: 'Team Player' },
    { name: 'FriendOne', compatibility: 87, reason: 'Complementary aggressive playstyle', style: 'Aggressive' },
    { name: 'FriendFour', compatibility: 72, reason: 'Similar champion pool and macro play', style: 'Macro Focused' },
    { name: 'FriendThree', compatibility: 65, reason: 'Balanced playstyles work well together', style: 'Balanced' }
  ];

  achievements = [
    { title: 'Most Games Played', winner: 'You', value: '1,247 games' },
    { title: 'Best Win Rate', winner: 'FriendTwo', value: '56.8%' },
    { title: 'Highest KDA', winner: 'FriendTwo', value: '3.5' },
    { title: 'Best Improvement', winner: 'You', value: '+47% KDA' }
  ];
}
