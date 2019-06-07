import { BaseApiEntityService } from './BaseApiEntity.service'
import { InputGeneratorDto } from '../shared/code/InputGeneratorDto'
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
export class GeneratorService extends BaseApiEntityService<InputGeneratorDto> {
  protected classRef = InputGeneratorDto

  constructor(http: HttpClient, config: Config, json: ClassTransformer) {
    super(http, config, json, 'generator')
  }

  public save(generator: InputGeneratorDto): Observable<number> {
    return this.http.post<number>(this.buildUrl(), this.json.serialize(generator))
  }

  public update(generator: InputGeneratorDto): Observable<any> {
    return this.http.put(this.buildUrl(generator.id), this.json.serialize(generator))
  }
}
