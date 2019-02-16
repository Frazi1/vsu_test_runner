import {HttpClient} from '@angular/common/http';
import {Config} from '../shared/Config';
import {JsonConvert} from 'json2typescript';
import {Observable} from 'rxjs/index';
import {TestInstance} from '../shared/instance/TestInstance';
import {map} from 'rxjs/internal/operators';
import {Injectable} from '@angular/core';
import {BaseService} from './base.service';
import {TestInstanceUpdate} from '../shared/instance/TestInstanceUpdate';

@Injectable({
  providedIn: 'root'
})
export class InstanceService extends BaseService {

  constructor(http: HttpClient,
              config: Config,
              json: JsonConvert) {
    super(http, config, json, 'instance');
  }

  public createTestInstance(templateId: number): Observable<number> {
    return this.http.post(`${this.endpoint}/create/${templateId}`, null)
      .pipe(
        map(res => +res)
      );
  }

  public getTestInstances(): Observable<TestInstance[]> {
    return this.http.get(this.endpoint)
      .pipe(
        map((values: any[]) => this.json.deserializeArray(values, TestInstance))
      );
  }

  public getTestInstance(id: number): Observable<TestInstance> {
    return this.http.get(`${this.endpoint}/${id}`)
      .pipe(
        map(res => this.json.deserialize(res, TestInstance))
      );
  }

  public updateTestInstance(id: number, testInstanceUpdate: TestInstanceUpdate): Observable<TestInstance> {
    return this.http.put(this.buildUrl(`${id}`), this.json.serialize(testInstanceUpdate))
      .pipe(
        map(res => this.json.deserialize(res, TestInstance))
      );
  }
}
