import { BaseService } from './base.service';
import { HttpClient } from '@angular/common/http';
import { JsonConvert } from 'json2typescript';
import { Config } from '../shared/Config';
import { Observable } from 'rxjs/index';
import { map } from 'rxjs/internal/operators';
import { Injectable } from '@angular/core';
import { TestRun } from '../shared/runner/TestRun';

@Injectable({
  'providedIn': 'root'
})
export class RunService extends BaseService {

  constructor(http: HttpClient, config: Config, json: JsonConvert) {
    super(http, config, json, 'run');
  }

  public startRunFromInstance(testInstanceId: number): Observable<number> {
    return this.http.post(`${this.endpoint}/${testInstanceId}`, null)
               .pipe(
                 map(res => +res)
               );
  }

  public getTestRun(testRunId: number): Observable<TestRun> {
    return this.getOne(testRunId, TestRun);
  }

  public getActiveTestRuns(): Observable<TestRun[]> {
    return this.http.get(this.buildUrl())
               .pipe(
                 map((res: any[]) => this.json.deserializeArray(res, TestRun))
               );
  }
}
