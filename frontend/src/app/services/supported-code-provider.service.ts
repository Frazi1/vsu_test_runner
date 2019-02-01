import {Injectable} from '@angular/core';
import {CodeType} from '../shared/CodeType';
import {Observable, of} from 'rxjs/index';
import {HttpClient} from '@angular/common/http';
import {Config} from '../shared/Config';
import {map, tap} from 'rxjs/internal/operators';

@Injectable({
  providedIn: 'root'
})
export class SupportedCodeProviderService {

  private _cache: CodeType[];

  constructor(private http: HttpClient, private config: Config) {
  }

  public codeTypes(): Observable<CodeType[]> {
    if (this._cache != null) {
      return of(this._cache);
    } else {
      return this.http.get(`${this.config.serverUrl}/code-types`)
        .pipe(
          map((values: any[]) => values.map(v => new CodeType(v))),
          map(values => values.slice(1)), // Remove VOID type
          tap(value => this._cache = value)
        );
    }
  }

}
