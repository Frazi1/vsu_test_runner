import { Injectable } from '@angular/core'
import { BaseApiEntityService } from './BaseApiEntity.service'
import { HttpClient } from '@angular/common/http'
import { Config } from '../shared/Config'
import { ClassTransformer } from 'class-transformer'
import { GroupDto } from '../shared/GroupDto'
import { Observable } from 'rxjs'

@Injectable({
  providedIn: 'root'
})
export class GroupService extends BaseApiEntityService<GroupDto> {
  protected classRef = GroupDto

  constructor(http: HttpClient, config: Config, json: ClassTransformer) {
    super(http, config, json, 'group')
  }

  public addGroup(group: GroupDto): Observable<number> {
    return this.http.post<number>(this.buildUrl(), this.json.serialize(group))
  }
}
