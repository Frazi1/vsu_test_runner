import { Injectable } from '@angular/core'
import { CodeType } from '../shared/CodeType'
import { Observable, timer } from 'rxjs'
import { HttpClient, HttpParams } from '@angular/common/http'
import { Config } from '../shared/Config'
import { map, shareReplay, switchMap, take } from 'rxjs/internal/operators'
import { BaseService } from './base.service'
import { CodeSnippetScaffoldingDto } from '../shared/code/CodeSnippetScaffoldingDto'
import { CodeLanguage } from '../shared/CodeLanguage'
import { CodeExecutionRequest } from '../shared/runner/CodeExecutionRequest'
import { CodeExecutionResponse } from '../shared/runner/CodeExecutionResponse'
import { ClassTransformer } from 'class-transformer'
import { ScaffoldingType } from '../shared/ScaffoldingType'
import { CodeExecutionResponseDto } from '../shared/runner/CodeExecutionResponseDto'

@Injectable({
  providedIn: 'root'
})
export class CodeService extends BaseService {

  constructor(http: HttpClient, config: Config, json: ClassTransformer) {
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
                              map((res) => this.json.plainToClass(CodeLanguage, res as Object[])),
                            )
        ),
        take(1),
        shareReplay(1)
      )
    }
    return this._languageCache$
  }

  public scaffoldFunction(functionId: number,
                          codeLanguage: CodeLanguage,
                          scaffoldingType: ScaffoldingType): Observable<CodeSnippetScaffoldingDto> {
    const opt = new HttpParams().append('language', codeLanguage.id)
                                .append('scaffoldingType', ScaffoldingType[scaffoldingType])
    return this.http.get(this.buildUrl('scaffold', functionId), {params: opt})
               .pipe(
                 map(res => this.json.plainToClass(CodeSnippetScaffoldingDto, res as Object))
               )
  }

  public scaffoldStartingSnippet(codeLanguage: CodeLanguage): Observable<CodeSnippetScaffoldingDto> {
    const opt = new HttpParams().append('language', codeLanguage.id)
    return this.http.get(this.buildUrl('scaffold'), {params: opt})
               .pipe(
                 map(res => this.json.plainToClass(CodeSnippetScaffoldingDto, res as Object))
               )
  }

  public getStartingSnippetForAnswer(codeLanguage: CodeLanguage,
                                     questionAnswerId: number): Observable<CodeSnippetScaffoldingDto> {
    const opt = new HttpParams().append('language', codeLanguage.id)
    return this.http.get(this.buildUrl('starting_snippet_for_answer', questionAnswerId), {params: opt})
               .pipe(
                 map(res => this.json.plainToClass(CodeSnippetScaffoldingDto, res as Object))
               )
  }

  public runCode(codeExecutionRequest: CodeExecutionRequest): Observable<CodeExecutionResponseDto[]> {
    return this.http.post(this.buildUrl('run'), this.json.serialize(codeExecutionRequest))
               .pipe(
                 map(res => this.json.plainToClass(CodeExecutionResponseDto, res as Object[]))
               )
  }

  public runTests(codeExecutionRequest: CodeExecutionRequest): Observable<CodeExecutionResponseDto[]> {
    return this.http.post(this.buildUrl('run_tests'), this.json.serialize(codeExecutionRequest))
               .pipe(
                 map(res => this.json.plainToClass(CodeExecutionResponseDto, res as Object[]))
               )
  }
}
