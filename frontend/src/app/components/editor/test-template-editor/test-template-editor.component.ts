import { Component, Inject, OnInit, Output, QueryList, ViewChildren } from '@angular/core'
import { ActivatedRoute, Router } from '@angular/router'
import { of, Subject, Subscription } from 'rxjs'
import { TestTemplate } from '../../../shared/TestTemplate'
import { TestQuestionTemplate } from '../../../shared/TestQuestionTemplate'
import { ITemplateService } from '../../../services/interfaces'
import { TestQuestionTemplateEditorComponent } from '../test-question-template-editor/test-question-template-editor.component'
import { debounceTime, switchMap, takeUntil, tap } from 'rxjs/operators'
import { CodeSnippet } from '../../../shared/CodeSnippet'
import { BaseComponent } from '../../base.component'

@Component({
  selector:    'app-test-template-editor',
  templateUrl: './test-template-editor.component.html',
  styleUrls:   ['./test-template-editor.component.scss']
})
export class TestTemplateEditorComponent extends BaseComponent implements OnInit {

  @Output()
  testTemplate: TestTemplate
  private paramSubscription: Subscription
  isCreating: boolean

  questionSearchQuery: string
  displayQuestions: TestQuestionTemplate[]
  currentQuestion: TestQuestionTemplate
  search$ = new Subject<string>()

  @ViewChildren(TestQuestionTemplateEditorComponent)
  private questionEditorComponents: QueryList<TestQuestionTemplateEditorComponent>

  constructor(private route: ActivatedRoute,
              @Inject('ITemplateService') private templatesService: ITemplateService,
              private router: Router) {
    super()
  }

  ngOnInit() {
    this.paramSubscription = this.route.params.pipe(
      switchMap(params => {
        const id = params['id']
        if (!id) {
          this.isCreating = true
          return of(new TestTemplate())
        } else {
          this.isCreating = false
          return this.templatesService.getTemplate(+id)
        }
      }),
      tap(res => this.testTemplate = res),
      tap(() => {
        if (this.testTemplate.questionTemplates.length === 0) {
          this.addQuestion()
        }
        this.selectQuestion(this.testTemplate.questionTemplates[0])
      }),
      tap(() => this.displayQuestions = this.testTemplate.questionTemplates)
    ).subscribe()

    this.search$.pipe(
      takeUntil(this.onDestroy$),
      // debounceTime(100),
      switchMap(query => of(this.searchQuestions(query, this.testTemplate.questionTemplates))),
      tap(res => this.displayQuestions = res)
    ).subscribe()
  }

  private searchQuestions(query: string, questions: TestQuestionTemplate[]): TestQuestionTemplate[] {
    return questions.filter(q => (q.name || '').toLowerCase().includes((query || '').toLowerCase()))
  }

  private addQuestion(): void {
    let testQuestionTemplate = new TestQuestionTemplate()
    testQuestionTemplate.name = 'Новый вопрос'
    testQuestionTemplate.codeSnippet = new CodeSnippet()
    this.testTemplate.questionTemplates.push(testQuestionTemplate)
    this.search$.next(this.questionSearchQuery)
  }

  private removeQuestion(q: TestQuestionTemplate) {
    this.testTemplate.questionTemplates = this.testTemplate.questionTemplates.filter(i => i !== q)
    if (this.currentQuestion === q) {
      this.selectQuestion(this.testTemplate.questionTemplates.length > 0
        ? this.testTemplate.questionTemplates[0]
        : null)
    }
    this.search$.next(this.questionSearchQuery)
  }

  private save(): void {
    this.onSave()
    if (this.isCreating) {
      this.add()
    } else {
      this.update()
    }
  }

  private add(): void {
    this.templatesService.addTemplate(this.testTemplate)
        .subscribe(id => this.router.navigate(['/template', id]))
  }

  private update(): void {
    const templateId = this.testTemplate.id
    this.templatesService.updateTemplate(this.testTemplate).pipe(
      switchMap(() => this.templatesService.getTemplate(templateId))
    ).subscribe(res => this.testTemplate = res)
  }

  private deleteTemplate(): void {
    if (this.isCreating === false) {
      this.templatesService.deleteTemplate(this.testTemplate.id)
          .subscribe(() => this.router.navigate(['/']))
    }
  }

  public onSave(): void {
    this.questionEditorComponents.forEach(qe => qe.onSave())
  }

  public selectQuestion(question: TestQuestionTemplate): void {
    this.currentQuestion = question
  }
}
