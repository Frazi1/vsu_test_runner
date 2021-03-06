import { Observable } from 'rxjs/index'
import { TestTemplate } from '../shared/TestTemplate'

export interface ITemplateService {
  getTemplate(id: number): Observable<TestTemplate>

  getTemplates(includeDeleted: boolean): Observable<TestTemplate[]>

  addTemplate(testTemplate: TestTemplate): Observable<number>

  updateTemplate(testTemplate: TestTemplate): Observable<number>

  deleteTemplate(id: number): Observable<any>

  restore(id: number): Observable<number>
}
