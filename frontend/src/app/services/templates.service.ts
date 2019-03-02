import { Injectable } from '@angular/core';
import { ITemplateService } from './interfaces';
import { Observable } from 'rxjs/index';
import { TestTemplate } from '../shared/TestTemplate';
import { HttpClient } from '@angular/common/http';
import { Config } from '../shared/Config';
import { map } from 'rxjs/internal/operators';
import { JsonConvert } from 'json2typescript';

@Injectable({
  providedIn: 'root'
})
export class TemplatesService implements ITemplateService {
  private _templatesUrl;

  constructor(private http: HttpClient,
              private config: Config,
              private jsonConvert: JsonConvert) {
    this._templatesUrl = config.serverUrl + '/template';
  }

  getTemplate(id: number): Observable<TestTemplate> {
    return this.http.get<TestTemplate>(`${this._templatesUrl}/${id}`)
               .pipe(
                 map(jsonValue => this.jsonConvert.deserialize(jsonValue, TestTemplate))
               );
  }

  getTemplates(): Observable<TestTemplate[]> {
    return this.http.get<TestTemplate[]>(this._templatesUrl)
               .pipe(
                 map((jsonValues: any[]) => this.jsonConvert.deserializeArray(jsonValues, TestTemplate))
               );
  }

  addTemplate(testTemplate: TestTemplate): Observable<number> {
    return this.http.post<number>(this._templatesUrl, this.jsonConvert.serialize(testTemplate));
  }

  updateTemplate(testTemplate: TestTemplate): Observable<TestTemplate> {
    const json = this.jsonConvert.serialize(testTemplate);
    return this.http.put<TestTemplate>(`${this._templatesUrl}/${testTemplate.id}`, json)
               .pipe(
                 map(jsonValue => this.jsonConvert.deserialize(jsonValue, TestTemplate))
               );
  }

  deleteTemplate(id: number): Observable<any> {
    return this.http.delete(`${this._templatesUrl}/${id}`);
  }

}
