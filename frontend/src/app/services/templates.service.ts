import {Injectable} from '@angular/core';
import {ITemplateService} from './interfaces';
import {Observable, of} from 'rxjs/index';
import {TestTemplate} from '../shared/TestTemplate';
import {HttpClient, HttpParams} from '@angular/common/http';
import {Config} from '../shared/Config';

@Injectable({
  providedIn: 'root'
})
export class TemplatesService implements ITemplateService {

  private _templatesUrl;

  constructor(private http: HttpClient,
              private config: Config) {
    this._templatesUrl = config.serverUrl + '/template';
  }

  getTemplate(id: number): Observable<TestTemplate> {
    return this.http.get<TestTemplate>(`${this._templatesUrl}/${id}`);
  }

  getTemplates(): Observable<TestTemplate[]> {
    return this.http.get<TestTemplate[]>(this._templatesUrl);
  }

  addTemplate(testTemplate: TestTemplate): Observable<number> {
    return this.http.post<number>(this._templatesUrl, testTemplate);
  }

  updateTemplate(testTemplate: TestTemplate): Observable<TestTemplate> {
    return this.http.put<TestTemplate>(`${this._templatesUrl}/${testTemplate.id}`, testTemplate);
  }
}
