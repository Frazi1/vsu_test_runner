import { Injectable } from '@angular/core'

@Injectable({
  providedIn: 'root'
})
export class Config {
  // private _serverUrl = 'http://localhost:8080'
  // private _serverUrl = 'http://localhost:63375/api'
  private _serverUrl = 'http://localhost:5000/api'
  // private _serverUrl = '..'

  public get serverUrl(): string {
    return this._serverUrl
  }
}
