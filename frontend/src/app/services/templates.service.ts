import { Injectable } from '@angular/core'
import { ITemplateService } from './interfaces'
import { Observable } from 'rxjs/index'
import { TestTemplate } from '../shared/TestTemplate'
import { HttpClient, HttpParams } from '@angular/common/http'
import { Config } from '../shared/Config'
import { map } from 'rxjs/internal/operators'
import { JsonConvert } from 'json2typescript'
import { BaseService } from './base.service'

@Injectable({
  providedIn: 'root'
})
export class TemplatesService extends BaseService implements ITemplateService {

  constructor(http: HttpClient,
              config: Config,
              jsonConvert: JsonConvert) {
    super(http, config, jsonConvert, 'template')
  }

  getTemplate(id: number): Observable<TestTemplate> {
    return this.http.get<TestTemplate>(this.buildUrl(id))
               .pipe(
                 map(jsonValue => this.json.deserialize(jsonValue, TestTemplate))
               )
  }

  getTemplates(includeDeleted: boolean = false): Observable<TestTemplate[]> {
    const params = new HttpParams().set('includeDeleted', includeDeleted.toString())
    return this.http.get<TestTemplate[]>(this.buildUrl(), {params: params})
               .pipe(
                 map((jsonValues: any[]) => this.json.deserializeArray(jsonValues, TestTemplate))
               )
  }

  addTemplate(testTemplate: TestTemplate): Observable<number> {
    return this.http.post<number>(this.buildUrl(), this.json.serialize(testTemplate))
  }

  updateTemplate(testTemplate: TestTemplate): Observable<TestTemplate> {
    const json = this.json.serialize(testTemplate)
    return this.http.put<TestTemplate>(this.buildUrl(testTemplate.id), json)
               .pipe(
                 map(jsonValue => this.json.deserialize(jsonValue, TestTemplate))
               )
  }

  deleteTemplate(id: number): Observable<any> {
    return this.http.delete(this.buildUrl(id))
  }

  public restore(id: number): Observable<number> {
    return this.http.put<number>(this.buildUrl('restore', id), null)
  }

}
