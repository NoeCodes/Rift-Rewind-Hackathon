import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PlayerDataService } from '../../services/player-data.service';
import { PlayerData } from '../../services/api.service';

@Component({
  selector: 'app-dashboard',
  imports: [CommonModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss'
})
export class Dashboard implements OnInit {
  playerName = 'Summoner';
  playerRank = 'Unranked';

  quickStats = [
    { label: 'Total Games', value: '0', icon: '🎮' },
    { label: 'Win Rate', value: '0%', icon: '🏆' },
    { label: 'Favorite Role', value: 'Unknown', icon: '⭐' },
    { label: 'Hours Played', value: '0', icon: '⏱️' }
  ];

  topChampions: any[] = [];

  constructor(private playerDataService: PlayerDataService) {}

  ngOnInit() {
    this.playerDataService.playerData$.subscribe((data: PlayerData | null) => {
      if (data) {
        this.updateDashboardWithPlayerData(data);
      }
    });
  }

  searchAnotherPlayer() {
    this.playerDataService.requestSearch();
  }

  updateDashboardWithPlayerData(data: PlayerData) {
    // Update player name and rank
    this.playerName = data.player_name;
    this.playerRank = `${data.ranked_status.tier} ${data.ranked_status.rank}`;

    // Update quick stats
    this.quickStats = [
      { label: 'Total Games', value: data.total_games.toString(), icon: '🎮' },
      { label: 'Win Rate', value: `${data.win_rate}%`, icon: '🏆' },
      { label: 'Favorite Role', value: data.favorite_role, icon: '⭐' },
      { label: 'Hours Played', value: data.hours_played.toString(), icon: '⏱️' }
    ];

    // Update top champions
    this.topChampions = Object.values(data.top_3_champions).map((champ: any) => ({
      name: champ.champion_name,
      games: champ.games_played,
      winRate: champ.win_rate,
      kda: champ.kda
    }));
  }
}
