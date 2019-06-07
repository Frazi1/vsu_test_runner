import { Injectable } from '@angular/core'

const ACCESS_TOKEN_KEY = 'accessToken'

@Injectable({
  providedIn: 'root'
})
export class AuthStorageService {

  private _accessToken: string

  constructor() { }

  public setAccessToken(token: string): void {
    this._accessToken = token
    localStorage.setItem(ACCESS_TOKEN_KEY, token)
  }

  public get accessToken(): string {
    if (this._accessToken == null) {
      this._accessToken = localStorage.getItem(ACCESS_TOKEN_KEY)
    }
    return this._accessToken
  }

  public get isAuthenticated(): boolean {
    return this.accessToken != null
  }

  public logout() {
    this._accessToken = null
    localStorage.removeItem(ACCESS_TOKEN_KEY)
  }
}
