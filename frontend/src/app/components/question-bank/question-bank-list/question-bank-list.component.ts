import { Component, OnInit } from '@angular/core'
import { QuestionBankService } from '../../../services/question-bank.service'
import { Observable, of, Subject } from 'rxjs'
import { QuestionBankSectionDto } from '../../../shared/question-bank/QuestionBankSectionDto'
import { BaseComponent } from '../../base.component'
import { catchError, map, switchMap, takeUntil, tap } from 'rxjs/operators'
import { Router } from '@angular/router'
import { QuestionTemplateService } from '../../../services/question-template.service'

@Component({
  selector:    'app-question-bank-list',
  templateUrl: './question-bank-list.component.html',
  styleUrls:   ['./question-bank-list.component.scss']
})
export class QuestionBankListComponent extends BaseComponent implements OnInit {

  newSectionName: string
  sections$: Observable<QuestionBankSectionDto[]>

  newSection$ = new Subject<void>()
  questionDelete$ = new Subject()

  constructor(private questionBankService: QuestionBankService,
              private questionService: QuestionTemplateService) {
    super()
  }

  private loadSections(): void {
    this.sections$ = this.questionBankService.getAll()
  }

  ngOnInit() {
    this.loadSections()
    this.newSection$.pipe(
      map(() => {
        let d = new QuestionBankSectionDto()
        d.name = this.newSectionName
        return d
      }),
      switchMap(s => this.questionBankService.addSection(s).pipe(catchError(of))),
      tap(() => this.loadSections())
    ).subscribe()

    this.questionDelete$.pipe(
      takeUntil(this.onDestroy$),
      switchMap((id: number) => this.questionService.deleteQuestion(id)),
      tap(() => this.loadSections())
    ).subscribe()
  }


}
