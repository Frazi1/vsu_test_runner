import { BaseService } from './base.service'
import { HttpClient } from '@angular/common/http'
import { Config } from '../shared/Config'
import { ClassTransformer } from 'class-transformer'
import { TestRun } from '../shared/runner/TestRun'
import { Observable } from 'rxjs'
import { map } from 'rxjs/operators'
import { Injectable } from '@angular/core'

@Injectable({
  'providedIn': 'root'
})
export class FinishedRunService extends BaseService {

  constructor(http: HttpClient, config: Config, json: ClassTransformer) {
    super(http, config, json, 'finished_run')
  }

  public getFinishedRuns(): Observable<TestRun[]> {
    return this.http.get(this.buildUrl()).pipe(
      map(res => this.json.plainToClass(TestRun, res as Object[]))
    )
  }

  public getFinishedRun(id: number): Observable<TestRun> {
    return this.get(this.buildUrl(id), TestRun)
  }
}
