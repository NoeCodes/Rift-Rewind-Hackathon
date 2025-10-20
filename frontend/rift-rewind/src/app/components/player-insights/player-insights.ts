import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-player-insights',
  imports: [CommonModule],
  templateUrl: './player-insights.html',
  styleUrl: './player-insights.scss'
})
export class PlayerInsights {
  strengths = [
    {
      title: 'Team Fighting',
      score: 92,
      description: 'You excel in team fights with excellent positioning',
      icon: '⚔️'
    },
    {
      title: 'Objective Control',
      score: 85,
      description: 'Strong dragon and baron control throughout the year',
      icon: '🐉'
    },
    {
      title: 'Vision Score',
      score: 88,
      description: 'Excellent map awareness and ward placement',
      icon: '👁️'
    }
  ];

  weaknesses = [
    {
      title: 'Early Game',
      score: 58,
      description: 'Opportunity to improve laning phase performance',
      icon: '🌅',
      tip: 'Focus on CS and trading in the first 10 minutes'
    },
    {
      title: 'Champion Pool',
      score: 62,
      description: 'Limited champion diversity in ranked games',
      icon: '🎭',
      tip: 'Try expanding to 2-3 more champions in your role'
    },
    {
      title: 'Death Prevention',
      score: 65,
      description: 'Average of 6.2 deaths per game - room for improvement',
      icon: '💀',
      tip: 'Work on positioning and map awareness'
    }
  ];

  growthAreas = [
    { month: 'January', improvement: 5 },
    { month: 'February', improvement: 8 },
    { month: 'March', improvement: 12 },
    { month: 'April', improvement: 15 },
    { month: 'May', improvement: 22 },
    { month: 'June', improvement: 28 },
    { month: 'July', improvement: 35 },
    { month: 'August', improvement: 38 },
    { month: 'September', improvement: 42 },
    { month: 'October', improvement: 45 },
    { month: 'November', improvement: 47 },
    { month: 'December', improvement: 47 }
  ];

  aiInsights = [
    {
      title: 'Peak Performance Time',
      insight: 'Your win rate is 12% higher in evening games (6PM-10PM)',
      recommendation: 'Schedule ranked games during evening hours for best results'
    },
    {
      title: 'Champion Synergy',
      insight: 'You perform 18% better when playing with engage supports',
      recommendation: 'Duo queue with tank/engage support players'
    },
    {
      title: 'Tilt Detection',
      insight: 'Win rate drops 23% after losing 2 games in a row',
      recommendation: 'Take a break after 2 consecutive losses'
    }
  ];
}
