import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { of, Subject } from 'rxjs'
import { IQuestion } from '../../shared/IQuestion'
import { startWith, switchMap, takeUntil, tap } from 'rxjs/operators'
import { BaseComponent } from '../base.component'

@Component({
  selector:    'app-question-list',
  templateUrl: './question-list.component.html',
  styleUrls:   ['./question-list.component.scss']
})
export class QuestionListComponent extends BaseComponent implements OnInit {

  @Input()
  questions: IQuestion[]

  @Output()
  questionsChange = new EventEmitter<IQuestion[]>()

  @Input()
  multiSelection: boolean = false

  @Input()
  allowDeletion: boolean = false

  @Input()
  selectedQuestions: IQuestion | IQuestion[]

  @Output()
  selectedQuestionsChange = new EventEmitter<IQuestion | IQuestion[]>()

  @Input()
  showSearch: boolean = true

  displayQuestions: IQuestion[]
  questionSearchQuery: string
  search$ = new Subject<string>()

  constructor() {super() }

  ngOnInit() {
    this.search$.pipe(
      takeUntil(this.onDestroy$),
      startWith(''),
      // debounceTime(100),
      switchMap(query => of(this.searchQuestions(query, this.questions))),
      tap(res => this.displayQuestions = res)
    ).subscribe()
  }

  private searchQuestions(query: string, questions: IQuestion[]): IQuestion[] {
    return questions.filter(q => (q.name || '').toLowerCase().includes((query || '').toLowerCase()))
  }


  public isSelected(question: IQuestion): boolean {
    if (!this.selectedQuestions) {
      return false
    }
    if (this.multiSelection === false) {
      return this.selectedQuestions === question
    } else {
      return (<IQuestion[]>this.selectedQuestions).some(q => q === question)
    }
  }

  public selectQuestion(q: IQuestion) {
    if (this.multiSelection) {
      if (!this.selectedQuestions) {
        this.selectedQuestions = []
      }
      (this.selectedQuestions as IQuestion[]).push(q)
    } else {
      this.selectedQuestions = q
    }
    this.selectedQuestionsChange.emit(this.selectedQuestions)
  }

  public removeQuestion(q: IQuestion) {
    this.questions = this.questions.filter(i => i !== q)
    if (this.selectedQuestions === q) {
      this.selectQuestion(this.questions.length > 0
        ? this.questions[0]
        : null)
    }
    this.search$.next(this.questionSearchQuery)
    this.questionsChange.emit(this.questions)
  }

  public hasDisplayItems(): boolean {
    return this.displayQuestions && this.displayQuestions.length > 0
  }

}
