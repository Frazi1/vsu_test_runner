export class AuthenticationResponseDto {
  accessToken: string
  refreshToken: string

  constructor(accessToken: string = null, refreshToken: string = null) {
    this.accessToken = accessToken
    this.refreshToken = refreshToken
  }
}
