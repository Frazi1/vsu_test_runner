import { Component, OnInit, ViewChild } from '@angular/core'
import { BaseComponent } from '../../base.component'
import { QuestionTemplateService } from '../../../services/question-template.service'
import { ActivatedRoute, Router } from '@angular/router'
import { TestQuestionTemplate } from '../../../shared/TestQuestionTemplate'
import { QuestionBankSectionDto } from '../../../shared/question-bank/QuestionBankSectionDto'
import { of, Subject } from 'rxjs'
import { catchError, switchMap, takeUntil, tap } from 'rxjs/operators'
import { CodeSnippet } from '../../../shared/CodeSnippet'
import { TestingInputParserService } from '../../../services/logic/testing-input-parser.service'
import { TestQuestionTemplateEditorComponent } from '../../editor/test-question-template-editor/test-question-template-editor.component'

@Component({
  selector:    'app-question-bank-question-editor',
  templateUrl: './question-bank-question-editor.component.html',
  styleUrls:   ['./question-bank-question-editor.component.scss']
})
export class QuestionBankQuestionEditorComponent extends BaseComponent implements OnInit {

  question: TestQuestionTemplate
  selectedSection: QuestionBankSectionDto

  creatingNew: boolean

  save$ = new Subject<number>()

  @ViewChild(TestQuestionTemplateEditorComponent)
  testQuestionEditor: TestQuestionTemplateEditorComponent

  constructor(private questionTemplateService: QuestionTemplateService,
              private route: ActivatedRoute,
              private router: Router) {
    super()
  }

  ngOnInit() {
    this.route.data.subscribe(d => {
      this.question = d.question
      this.creatingNew = d.creatingNew

      if (this.creatingNew === true) {
        this.question = new TestQuestionTemplate()
        this.question.codeSnippet = new CodeSnippet()
      }
    })

    this.saveSub()
  }

  private saveSub() {
    this.save$.pipe(
      takeUntil(this.onDestroy$),
      tap(() => this.testQuestionEditor.onSave()),
      switchMap(() => this.questionTemplateService.addQuestion(
        this.question).pipe(catchError(() => of()))),
      tap(id => this.router.navigate(['..', id, 'edit']))
    ).subscribe()
  }

  onSectionChanged(newSection: QuestionBankSectionDto) {
    this.question.questionBankSectionId = newSection.id
  }

}
