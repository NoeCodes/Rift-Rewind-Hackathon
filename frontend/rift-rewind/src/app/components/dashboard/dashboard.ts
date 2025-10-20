import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule, RouterLink],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})
export class Dashboard {
  playerName = 'Summoner123';
  playerRank = 'Gold II';

  quickStats = [
    { label: 'Total Games', value: '1,247', icon: '🎮' },
    { label: 'Win Rate', value: '54.3%', icon: '🏆' },
    { label: 'Favorite Role', value: 'Mid Lane', icon: '⭐' },
    { label: 'Hours Played', value: '487', icon: '⏱️' }
  ];

  topChampions = [
    { name: 'Ahri', games: 156, winRate: 58, kda: 3.4 },
    { name: 'Yasuo', games: 142, winRate: 52, kda: 2.9 },
    { name: 'Zed', games: 128, winRate: 56, kda: 3.1 }
  ];

  recentActivity = [
    { date: 'Today', action: 'Completed 5 ranked games', result: '3W - 2L' },
    { date: 'Yesterday', action: 'Achieved Gold II rank', result: 'Promotion' },
    { date: '2 days ago', action: 'Pentakill with Ahri', result: 'Victory' }
  ];
}
