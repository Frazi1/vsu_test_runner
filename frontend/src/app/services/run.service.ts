import { BaseService } from './base.service'
import { HttpClient } from '@angular/common/http'
import { Config } from '../shared/Config'
import { Observable } from 'rxjs/index'
import { map } from 'rxjs/internal/operators'
import { Injectable } from '@angular/core'
import { TestRun } from '../shared/runner/TestRun'
import { ClassTransformer } from 'class-transformer'
import { TestRunAnswerUpdate } from '../shared/runner/TestRunAnswerUpdate'

@Injectable({
  'providedIn': 'root'
})
export class RunService extends BaseService {

  constructor(http: HttpClient, config: Config, json: ClassTransformer) {
    super(http, config, json, 'run')
  }

  public startRunFromInstance(testInstanceId: number): Observable<number> {
    return this.http.post(`${this.endpoint}/${testInstanceId}`, null)
               .pipe(
                 map(res => +res)
               )
  }

  public getTestRun(testRunId: number): Observable<TestRun> {
    return this.getOne(testRunId, TestRun)
  }

  public getActiveTestRuns(): Observable<TestRun[]> {
    return this.http.get(this.buildUrl())
               .pipe(
                 map(res => this.json.plainToClass(TestRun, res as Object[]))
               )
  }

  public updateTestRunAnswers(testRunId: number, updates: TestRunAnswerUpdate[]): Observable<TestRun> {
    return this.put(this.buildUrl(testRunId), updates, TestRun)
  }
}
