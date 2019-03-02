import { JsonConvert } from 'json2typescript'
import { Config } from '../shared/Config'
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http'
import { Observable } from 'rxjs/index'
import { map } from 'rxjs/internal/operators'

export class BaseService {
  private _endpoint: string

  get endpoint(): string {
    return this._endpoint
  }

  constructor(protected http: HttpClient,
              private config: Config,
              protected json: JsonConvert,
              protected endpointPostfix) {
    this._endpoint = `${this.config.serverUrl}/${endpointPostfix}`
  }

  protected buildUrl(...args: (string | number)[]): string {
    let url = this.endpoint
    if (!url.endsWith('/') && args.length > 0) {
      url += '/'
    }
    return url + args.join('/')
  }

  protected getOne<T>(id: number, classRef: { new(): T; }): Observable<T> {
    return this.http.get(this.buildUrl(`${id}`))
               .pipe(
                 map(res => this.json.deserialize(res, classRef))
               )
  }

  protected put<T, U>(url: string,
                      body: T,
                      classRef: { new(): U },
                      options?: { params?: HttpParams, headers?: HttpHeaders }): Observable<U> {
    return this.http.put<number>(url, this.json.serialize(body), options)
               .pipe(
                 map(res => this.deserialize(res, classRef))
               )
  }

  private deserialize<T>(res: any | any[], classRef: { new(): T }) {
    return classRef.isPrototypeOf(Array)
      ? this.json.deserializeArray(res as any[], classRef)
      : this.json.deserialize(res, classRef)
  }
}
