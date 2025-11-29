import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { PlayerData } from './api.service';

@Injectable({
  providedIn: 'root'
})
export class PlayerDataService {
  private playerDataSubject = new BehaviorSubject<PlayerData | null>(null);
  public playerData$: Observable<PlayerData | null> = this.playerDataSubject.asObservable();

  constructor() { }

  setPlayerData(data: PlayerData) {
    this.playerDataSubject.next(data);
  }

  getPlayerData(): PlayerData | null {
    return this.playerDataSubject.value;
  }

  clearPlayerData() {
    this.playerDataSubject.next(null);
  }
}
