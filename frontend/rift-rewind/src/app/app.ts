import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterLink, RouterLinkActive, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService } from './services/api.service';
import { PlayerDataService } from './services/player-data.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    RouterLink,
    RouterLinkActive,
    FormsModule
  ],
  templateUrl: './app.html',
  styleUrls: ['./app.scss']
})
export class App {
  searchName: string = '';
  searchTag: string = '';
  filteredPlayers: any[] = [];
  showSearchScreen: boolean = true;
  isLoading: boolean = false;
  errorMessage: string = '';

  constructor(
    private apiService: ApiService,
    private playerDataService: PlayerDataService,
    private router: Router
  ) {}

  searchPlayer() {
    const name = this.searchName.trim().toLowerCase();
    const tag = this.searchTag.trim().toLowerCase();

    const mockPlayers = [
      { name: 'Wilson', tag: 'Ethan' },
      { name: 'Noe', tag: 'Yuvaraj' },
      { name: 'Daniel', tag: 'Khizzer' },
      { name: 'Abdullah', tag: 'Zane' },
    ];

    if (!name && !tag) {
      this.filteredPlayers = [];
      return;
    }

    this.filteredPlayers = mockPlayers.filter(p =>
      p.name.toLowerCase().includes(name) &&
      p.tag.toLowerCase().includes(tag)
    );
  }

  exitSearch() {
    if (!this.searchName.trim() || !this.searchTag.trim()) {
      this.errorMessage = 'Please enter both player name and tag';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    this.apiService.getPlayerData(this.searchName.trim(), this.searchTag.trim())
      .subscribe({
        next: (data) => {
          this.playerDataService.setPlayerData(data);
          this.isLoading = false;
          this.showSearchScreen = false;
          this.router.navigate(['/dashboard']);
        },
        error: (error) => {
          this.isLoading = false;
          this.errorMessage = error.message || 'Failed to fetch player data. Please try again.';
          console.error('Error fetching player data:', error);
        }
      });
  }
}
