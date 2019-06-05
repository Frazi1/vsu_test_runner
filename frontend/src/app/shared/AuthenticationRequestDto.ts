export class AuthenticationRequestDto {
  userName: string
  password: string

  constructor(userName: string = null, password: string = null) {
    this.userName = userName
    this.password = password
  }
}
