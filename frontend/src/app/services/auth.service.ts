import { Injectable } from '@angular/core'
import { BaseService } from './base.service'
import { HttpClient, HttpParams } from '@angular/common/http'
import { Config } from '../shared/Config'
import { ClassTransformer } from 'class-transformer'
import { Observable } from 'rxjs'
import { SignUpRequestDto } from '../shared/SignUpRequestDto'
import { AuthenticationRequestDto } from '../shared/AuthenticationRequestDto'
import { map } from 'rxjs/operators'
import { AuthenticationResponseDto } from '../shared/AuthenticationResponseDto'

@Injectable({
  providedIn: 'root'
})
export class AuthService extends BaseService {
  constructor(http: HttpClient, config: Config, json: ClassTransformer) {
    super(http, config, json, 'auth')
  }

  public isUsernameTaken(username: string): Observable<boolean> {
    let options = {
      params: new HttpParams().append('username', username)
    }
    return this.http.get<boolean>(this.buildUrl('check_username'), options)
  }

  public signUp(request: SignUpRequestDto): Observable<any> {
    return this.http.post(this.buildUrl('signup'), this.json.serialize(request))
  }

  public authenticate(request: AuthenticationRequestDto): Observable<AuthenticationResponseDto> {
    return this.http.post(this.buildUrl(), this.json.serialize(request)).pipe(
      map(res => this.json.plainToClass(AuthenticationResponseDto, res as Object))
    )
  }
}
