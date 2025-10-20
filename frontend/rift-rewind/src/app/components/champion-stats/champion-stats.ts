import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-champion-stats',
  imports: [CommonModule, FormsModule],
  templateUrl: './champion-stats.html',
  styleUrl: './champion-stats.scss'
})
export class ChampionStats {
  champions = [
    { name: 'Ahri', role: 'Mid', games: 156, wins: 90, losses: 66, winRate: 58, kda: 3.4, cs: 7.2, gold: '11.2k' },
    { name: 'Yasuo', role: 'Mid', games: 142, wins: 74, losses: 68, winRate: 52, kda: 2.9, cs: 7.8, gold: '11.8k' },
    { name: 'Zed', role: 'Mid', games: 128, wins: 72, losses: 56, winRate: 56, kda: 3.1, cs: 7.5, gold: '11.5k' },
    { name: 'Katarina', role: 'Mid', games: 95, wins: 52, losses: 43, winRate: 55, kda: 3.3, cs: 6.8, gold: '10.9k' },
    { name: 'Akali', role: 'Mid', games: 87, wins: 45, losses: 42, winRate: 52, kda: 2.8, cs: 6.9, gold: '10.7k' },
    { name: 'Sylas', role: 'Mid', games: 76, wins: 48, losses: 28, winRate: 63, kda: 3.8, cs: 7.1, gold: '11.4k' }
  ];

  selectedRole = 'All';
  sortBy = 'games';

  roles = ['All', 'Top', 'Jungle', 'Mid', 'ADC', 'Support'];

  get filteredChampions() {
    let filtered = this.champions;

    if (this.selectedRole !== 'All') {
      filtered = filtered.filter(c => c.role === this.selectedRole);
    }

    return filtered.sort((a, b) => {
      if (this.sortBy === 'games') return b.games - a.games;
      if (this.sortBy === 'winRate') return b.winRate - a.winRate;
      if (this.sortBy === 'kda') return b.kda - a.kda;
      return 0;
    });
  }

  selectRole(role: string) {
    this.selectedRole = role;
  }

  selectSort(sort: string) {
    this.sortBy = sort;
  }
}
