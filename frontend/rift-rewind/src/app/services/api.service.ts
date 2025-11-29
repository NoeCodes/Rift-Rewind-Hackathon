import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

export interface PlayerData {
  player_name: string;
  tag_line: string;
  puuid: string;
  total_games: number;
  win_rate: number;
  hours_played: number;
  favorite_role: string;
  ranked_status: {
    tier: string;
    rank: string;
  };
  top_3_champions: {
    [key: string]: {
      champion_name: string;
      champion_initial: string;
      games_played: number;
      win_rate: number;
      kda: number;
    };
  };
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) { }

  getPlayerData(gameName: string, tagLine: string): Observable<PlayerData> {
    const url = `${this.baseUrl}/player/${gameName}/${tagLine}`;
    return this.http.get<PlayerData>(url).pipe(
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse) {
    let errorMessage = 'An error occurred';

    if (error.error instanceof ErrorEvent) {
      // Client-side error
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Server-side error
      errorMessage = error.error?.message || `Error Code: ${error.status}\nMessage: ${error.message}`;
    }

    return throwError(() => new Error(errorMessage));
  }
}
