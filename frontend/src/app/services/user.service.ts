import { Injectable } from '@angular/core'
import { BaseApiEntityService } from './BaseApiEntity.service'
import { UserDto } from '../shared/UserDto'
import { ClassTransformer } from 'class-transformer'
import { Config } from '../shared/Config'
import { HttpClient } from '@angular/common/http'

@Injectable({
  providedIn: 'root'
})
export class UserService extends BaseApiEntityService<UserDto> {

  protected classRef = UserDto


  constructor(http: HttpClient, config: Config, json: ClassTransformer) {
    super(http, config, json, 'user')
  }
}
