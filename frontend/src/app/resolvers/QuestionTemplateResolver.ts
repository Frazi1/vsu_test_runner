import { ActivatedRouteSnapshot, Resolve, RouterStateSnapshot } from '@angular/router'
import { TestQuestionTemplate } from '../shared/TestQuestionTemplate'
import { Observable } from 'rxjs'
import { QuestionTemplateService } from '../services/question-template.service'
import { Injectable } from '@angular/core'

@Injectable()
export class QuestionTemplateResolver implements Resolve<TestQuestionTemplate> {
  constructor(private questionTemplateService: QuestionTemplateService) {

  }

  public resolve(route: ActivatedRouteSnapshot,
                 state: RouterStateSnapshot): Observable<TestQuestionTemplate> | Promise<TestQuestionTemplate> | TestQuestionTemplate {
    // const templateId = +route.paramMap.get('questionTemplateId')
    const templateId = +route.paramMap.get('questionTemplateId')
    return this.questionTemplateService.getById(templateId)
  }

}
