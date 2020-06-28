import { Injectable } from '@angular/core'
import { BaseApiEntityService } from './BaseApiEntity.service'
import { QuestionBankSectionDto } from '../shared/question-bank/QuestionBankSectionDto'
import { HttpClient } from '@angular/common/http'
import { Config } from '../shared/Config'
import { ClassTransformer } from 'class-transformer'
import { Observable } from 'rxjs'
import { map } from 'rxjs/operators'

@Injectable({
  providedIn: 'root'
})
export class QuestionBankService extends BaseApiEntityService<QuestionBankSectionDto> {
  protected classRef = QuestionBankSectionDto


  constructor(http: HttpClient,
              config: Config,
              json: ClassTransformer) {
    super(http, config, json, 'questionBank')
  }

  public getSectionHeaders(): Observable<QuestionBankSectionDto[]> {
    return this.http.get(this.buildUrl('headers')).pipe(
      map(res => this.transformMany(res as Object[]))
    )
  }

  public addSection(section: QuestionBankSectionDto): Observable<number> {
    return this.http.post<number>(this.buildUrl(), this.json.serialize(section))
  }
}
