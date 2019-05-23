import { BaseApiEntityService } from './BaseApiEntity.service'
import { TestingInputGeneratorDto } from '../shared/code/TestingInputGeneratorDto'
import { HttpClient } from '@angular/common/http'
import { Config } from '../shared/Config'
import { ClassTransformer } from 'class-transformer'
import { Injectable } from '@angular/core'
import { TestRun } from '../shared/runner/TestRun'
import { Test } from 'tslint'
import { BaseService } from './base.service'
import { map } from 'rxjs/operators'
import { Observable } from 'rxjs'

@Injectable({
  providedIn: 'root'
})
export class TestingInputGeneratorService extends BaseApiEntityService<TestingInputGeneratorDto> {
  protected classRef = TestingInputGeneratorDto

  constructor(http: HttpClient, config: Config, json: ClassTransformer) {
    super(http, config, json, 'generator')
  }

  public save(generator: TestingInputGeneratorDto): Observable<number> {
    return this.http.post<number>(this.buildUrl(), this.json.serialize(generator))
  }
}
