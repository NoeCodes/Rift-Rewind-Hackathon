import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet, RouterLink, RouterLinkActive } from '@angular/router';
import { FormsModule } from '@angular/forms';

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
    this.showSearchScreen = false;
  }
}
