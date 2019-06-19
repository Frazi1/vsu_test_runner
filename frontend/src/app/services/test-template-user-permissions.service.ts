import { Injectable } from '@angular/core'
import { BaseApiEntityService } from './BaseApiEntity.service'
import { TestTemplateUserPermissionsDto } from '../shared/TestTemplateUserPermissionsDto'
import { ClassTransformer } from 'class-transformer'
import { Config } from '../shared/Config'
import { HttpClient } from '@angular/common/http'
import { Observable } from 'rxjs'
import { map } from 'rxjs/operators'

@Injectable({
  providedIn: 'root'
})
export class TestTemplateUserPermissionsService extends BaseApiEntityService<TestTemplateUserPermissionsDto> {
  protected classRef = TestTemplateUserPermissionsDto


  constructor(http: HttpClient,
              config: Config,
              json: ClassTransformer,
  ) {
    super(http, config, json, 'testTemplatePermissions')
  }

  public getByTestTemplateId(testTemplateId: number): Observable<TestTemplateUserPermissionsDto[]> {
    return this.http.get(this.buildUrl(testTemplateId)).pipe(
      map((res: any[]) => this.transformMany(res))
    )
  }

  public updateByTestTemplateId(testTemplateId: number, permissions: TestTemplateUserPermissionsDto[]): Observable<any> {
    return this.http.put(this.buildUrl(testTemplateId), this.json.serialize(permissions))
  }
}
