import { ClassTransformer } from 'class-transformer'
import { Config } from '../shared/Config'
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http'
import { Observable } from 'rxjs'
import { map } from 'rxjs/internal/operators'

export class BaseService {
  private _endpoint: string

  constructor(protected http: HttpClient,
              private config: Config,
              protected json: ClassTransformer,
              protected endpointPostfix) {
    this._endpoint = `${this.config.serverUrl}/${endpointPostfix}`
  }

  get endpoint(): string {
    return this._endpoint
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
                 map(res => this.json.plainToClass(classRef, res as Object))
               )
  }

  protected put<T, U>(url: string,
                      body: T,
                      classRef: { new(): U },
                      options?: { params?: HttpParams, headers?: HttpHeaders }): Observable<U> {
    return this.http.put(url, this.json.serialize(body), options)
               .pipe(
                 map(res => this.json.plainToClass(classRef, res as Object))
               )
  }

  protected get<TResult>(url: string,
                         classRef: { new(): TResult },
                         options?: { params?: HttpParams, headers?: HttpHeaders }): Observable<TResult> {
    return this.http.get(url, options)
               .pipe(
                 map(res => this.json.plainToClass(classRef, res as Object))
               )
  }
}
