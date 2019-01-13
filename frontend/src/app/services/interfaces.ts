import {Observable} from 'rxjs/index';
import {TestTemplate} from '../shared/TestTemplate';

export interface ITemplateService {
  getTemplate(id: number): Observable<TestTemplate>;

  getTemplates(): Observable<TestTemplate[]>;

  addTemplate(testTemplate: TestTemplate): Observable<number>;
}
