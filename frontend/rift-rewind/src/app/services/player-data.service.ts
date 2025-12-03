import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, Subject } from 'rxjs';
import { PlayerData } from './api.service';

@Injectable({
  providedIn: 'root'
})
export class PlayerDataService {
  private playerDataSubject = new BehaviorSubject<PlayerData | null>(null);
  public playerData$: Observable<PlayerData | null> = this.playerDataSubject.asObservable();

  private searchRequestSubject = new Subject<void>();
  public searchRequest$: Observable<void> = this.searchRequestSubject.asObservable();

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

  requestSearch() {
    this.searchRequestSubject.next();
  }
}
