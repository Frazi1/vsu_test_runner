import { Injectable } from '@angular/core'

const ACCESS_TOKEN_KEY = 'accessToken'
const USER_NAME = 'userName'

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

  public setUsername(userName: string): void {
    localStorage.setItem(USER_NAME, userName)
  }

  public getUsername(): string {
    return localStorage.getItem(USER_NAME)
  }

  public get isAuthenticated(): boolean {
    return this.accessToken != null
  }

  public logout() {
    this._accessToken = null
    localStorage.removeItem(ACCESS_TOKEN_KEY)
  }
}
