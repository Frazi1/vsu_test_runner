import { Injectable } from '@angular/core'
import { CodeType } from '../shared/CodeType'
import { Observable, timer } from 'rxjs/index'
import { HttpClient, HttpParams } from '@angular/common/http'
import { Config } from '../shared/Config'
import { map, shareReplay, switchMap, take } from 'rxjs/internal/operators'
import { BaseService } from './base.service'
import { JsonConvert } from 'json2typescript'
import { FunctionScaffoldingDto } from '../shared/code/FunctionScaffoldingDto'
import { CodeLanguage } from '../shared/CodeLanguage'
import { CodeExecutionRequest } from '../shared/runner/CodeExecutionRequest'
import { CodeExecutionResponse } from '../shared/runner/CodeExecutionResponse'

@Injectable({
  providedIn: 'root'
})
export class CodeService extends BaseService {

  constructor(http: HttpClient, config: Config, json: JsonConvert) {
    super(http, config, json, 'code')
  }

  private CACHE_REFRESH_INTERVAL = 10 * 1000 * 10 // 10 minutes

  private _languageCache$: Observable<CodeLanguage[]>
  private _typeCache$: Observable<CodeType[]>


  public codeTypes(): Observable<CodeType[]> {
    if (!this._typeCache$) {
      const timer$ = timer(0, this.CACHE_REFRESH_INTERVAL)
      this._typeCache$ = timer$.pipe(
        switchMap(() => this.http.get(this.buildUrl('types')).pipe(
          map((values: any[]) => values.map(v => new CodeType(v))),
          map(values => values.slice(1)) // Remove VOID type
          )
        ),
        take(1),
        shareReplay(1)
      )
    }
    return this._typeCache$
  }

  public languages(): Observable<CodeLanguage[]> {
    if (!this._languageCache$) {
      const timer$ = timer(0, this.CACHE_REFRESH_INTERVAL)
      this._languageCache$ = timer$.pipe(
        switchMap(() => this.http.get(this.buildUrl('languages'))
                            .pipe(
                              map((res: string[]) => res.map(langName => new CodeLanguage(langName))),
                            )
        ),
        take(1),
        shareReplay(1)
      )
    }
    return this._languageCache$
  }

  public scaffoldFunction(functionId: number, codeLanguage: CodeLanguage): Observable<FunctionScaffoldingDto> {
    const opt = new HttpParams().append('language', codeLanguage.name)
    return this.http.get(this.buildUrl('scaffold', functionId), {params: opt})
               .pipe(
                 map(res => this.json.deserialize(res, FunctionScaffoldingDto))
               )
  }

  public runCode(codeExecutionRequest: CodeExecutionRequest): Observable<CodeExecutionResponse> {
    return this.http.post(this.buildUrl('run'), this.json.serialize(codeExecutionRequest))
               .pipe(
                 map(res => this.json.deserialize(res, CodeExecutionResponse))
               )
  }
}