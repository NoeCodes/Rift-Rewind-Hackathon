import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { ApiService } from './services/api.service';
import { PlayerDataService } from './services/player-data.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    FormsModule
  ],
  templateUrl: './app.html',
  styleUrls: ['./app.scss']
})
export class App {
  searchName: string = '';
  searchTag: string = '';
  showSearchScreen: boolean = true;
  isLoading: boolean = false;
  errorMessage: string = '';

  constructor(
    private apiService: ApiService,
    private playerDataService: PlayerDataService,
    private router: Router
  ) {
    this.playerDataService.searchRequest$.subscribe(() => {
      this.showSearchScreen = true;
      this.searchName = '';
      this.searchTag = '';
      this.errorMessage = '';
    });
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
