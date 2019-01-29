import {Injectable} from '@angular/core';
import {TestTemplate} from '../shared/TestTemplate';
import {Observable, of} from 'rxjs/index';
import {TestQuestionTemplate} from '../shared/TestQuestionTemplate';
import {ITemplateService} from './interfaces';

@Injectable({
  providedIn: 'root'
})
export class MockTemplatesService implements ITemplateService {

  templates = [
    new TestTemplate(1, '123', null, [new TestQuestionTemplate('q1'), new TestQuestionTemplate('q2')]),
    new TestTemplate(2, '345'),
    new TestTemplate(3, '678')];

  constructor() {
  }

  public getTemplates(): Observable<TestTemplate[]> {
    return of(this.templates);
  }

  public getTemplate(id: number): Observable<TestTemplate> {
    return of(this.templates[id - 1]);
  }

  public addTemplate(testTemplate: TestTemplate): Observable<number> {
    testTemplate.id = this.templates.length + 1;
    this.templates.push(testTemplate);
    return of(testTemplate.id);
  }


  updateTemplate(testTemplate: TestTemplate): Observable<TestTemplate> {
    return null;
  }

  deleteTemplate(id: number): Observable<any> {
    return undefined;
  }
}
