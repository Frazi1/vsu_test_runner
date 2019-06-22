import { Injectable } from '@angular/core'
import { BaseApiEntityService } from './BaseApiEntity.service'
import { TestQuestionTemplate } from '../shared/TestQuestionTemplate'
import { HttpClient } from '@angular/common/http'
import { Config } from '../shared/Config'
import { ClassTransformer } from 'class-transformer'
import { Observable } from 'rxjs'

@Injectable({
  providedIn: 'root'
})
export class QuestionTemplateService extends BaseApiEntityService<TestQuestionTemplate> {
  protected classRef = TestQuestionTemplate


  constructor(http: HttpClient, config: Config, json: ClassTransformer) {
    super(http, config, json, 'questionTemplate')
  }

  public addQuestion(question: TestQuestionTemplate): Observable<number> {
    return this.http.post<number>(this.buildUrl(), this.json.serialize(question))
  }
}
