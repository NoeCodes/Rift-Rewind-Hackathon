import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-year-recap',
  imports: [CommonModule],
  templateUrl: './year-recap.html',
  styleUrl: './year-recap.scss'
})
export class YearRecap {
  currentSlide = 0;

  slides = [
    {
      title: 'Your 2024 Journey',
      subtitle: 'A year of legends in the making',
      content: 'You played 1,247 games this year!',
      emoji: '🎮',
      highlight: '1,247 Games'
    },
    {
      title: 'Most Played Champion',
      subtitle: 'Your signature pick',
      content: 'You dominated the Rift with Ahri across 156 games',
      emoji: '⭐',
      highlight: 'Ahri - 156 Games'
    },
    {
      title: 'Epic Moments',
      subtitle: 'Unforgettable plays',
      content: 'You scored 12 Pentakills this year!',
      emoji: '🔥',
      highlight: '12 Pentakills'
    },
    {
      title: 'Biggest Improvement',
      subtitle: 'Your growth story',
      content: 'Your KDA improved by 47% this year',
      emoji: '📈',
      highlight: '+47% KDA'
    },
    {
      title: 'Time Invested',
      subtitle: 'Dedication to the grind',
      content: 'You spent 487 hours in the Rift',
      emoji: '⏱️',
      highlight: '487 Hours'
    },
    {
      title: 'Rank Achievement',
      subtitle: 'Your competitive journey',
      content: 'Climbed from Silver III to Gold II',
      emoji: '💎',
      highlight: 'Gold II Achieved'
    }
  ];

  nextSlide() {
    if (this.currentSlide < this.slides.length - 1) {
      this.currentSlide++;
    }
  }

  prevSlide() {
    if (this.currentSlide > 0) {
      this.currentSlide--;
    }
  }

  shareRecap() {
    alert('Share functionality would be implemented here! This would generate a shareable image or link to your recap.');
  }
}
