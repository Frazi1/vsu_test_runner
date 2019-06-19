import { Injectable } from '@angular/core'
import { BaseService } from './base.service'
import { HttpClient } from '@angular/common/http'
import { Config } from '../shared/Config'
import { ClassTransformer } from 'class-transformer'
import { Observable } from 'rxjs'
import { map } from 'rxjs/operators'
import { ActiveDirectorySearchRequestDto } from '../shared/ActiveDirectorySearchRequestDto'
import { UserDto } from '../shared/UserDto'

@Injectable({
  providedIn: 'root'
})
export class LdapIntegrationService extends BaseService {


  constructor(http: HttpClient, config: Config, json: ClassTransformer) {
    super(http, config, json, 'LdapIntegration')
  }

  public getUserProperties(): Observable<string[]> {
    return this.http.get(this.buildUrl('user_properties')).pipe(
      map(res => res as string[])
    )
  }

  public searcADForUsers(request: ActiveDirectorySearchRequestDto): Observable<UserDto[]> {
    return this.http.post(this.buildUrl(), this.json.serialize(request)).pipe(
      map(res => this.json.plainToClass(UserDto, res as Object[]))
    )
  }
}
