import { Injectable } from '@angular/core';
import { CodeType } from '../shared/CodeType';
import { Observable, of } from 'rxjs/index';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Config } from '../shared/Config';
import { map, tap } from 'rxjs/internal/operators';
import { BaseService } from './base.service';
import { JsonConvert } from 'json2typescript';
import { FunctionScaffoldingDto } from '../shared/code/FunctionScaffoldingDto';
import { CodeLanguage } from '../shared/CodeLanguage';
import { CodeExecutionRequest } from '../shared/runner/CodeExecutionRequest';
import { CodeExecutionResponse } from '../shared/runner/CodeExecutionResponse';

@Injectable({
  providedIn: 'root'
})
export class CodeService extends BaseService {

  constructor(http: HttpClient, config: Config, json: JsonConvert) {
    super(http, config, json, 'code');
  }

  private _cache: CodeType[];
  private _languageCache: CodeLanguage[];

  public codeTypes(): Observable<CodeType[]> {
    if (this._cache != null) {
      return of(this._cache);
    } else {
      return this.http.get(this.buildUrl('types'))
                 .pipe(
                   map((values: any[]) => values.map(v => new CodeType(v))),
                   map(values => values.slice(1)), // Remove VOID type
                   tap(value => this._cache = value)
                 );
    }
  }

  public languages(): Observable<CodeLanguage[]> {
    if (this._languageCache) {
      return of(this._languageCache);
    } else {
      return this.http.get(this.buildUrl('languages'))
                 .pipe(
                   map((res: string[]) => res.map(langName => new CodeLanguage(langName))),
                   tap(res => this._languageCache = res)
                 );
    }
  }

  public scaffoldFunction(functionId: number, codeLanguage: CodeLanguage): Observable<FunctionScaffoldingDto> {
    const opt = new HttpParams().append('language', codeLanguage.name);
    return this.http.get(this.buildUrl('scaffold', functionId), {params: opt})
               .pipe(
                 map(res => this.json.deserialize(res, FunctionScaffoldingDto))
               );
  }

  public runCode(codeExecutionRequest: CodeExecutionRequest): Observable<CodeExecutionResponse> {
    return this.http.post(this.buildUrl('run'), this.json.serialize(codeExecutionRequest))
               .pipe(
                 map(res => this.json.deserialize(res, CodeExecutionResponse))
               );
  }
}
