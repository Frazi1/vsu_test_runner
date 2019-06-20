import { Component, OnDestroy, OnInit } from '@angular/core'
import { RunService } from '../../../services/run.service'
import { ActivatedRoute, Router } from '@angular/router'
import { merge, Observable, Subject, timer } from 'rxjs'
import { TestRun } from '../../../shared/runner/TestRun'
import { QuestionAnswer } from '../../../shared/runner/QuestionAnswer'
import { TestRunAnswerUpdate } from '../../../shared/runner/TestRunAnswerUpdate'
import {
  concatMap, distinctUntilChanged, filter, map, mergeMap, retry, switchMap, takeUntil, takeWhile, tap,
} from 'rxjs/internal/operators'
import * as moment from 'moment'

@Component({
  selector:    'app-test-runner',
  templateUrl: './test-runner.component.html',
  styleUrls:   ['./test-runner.component.scss']
})
export class TestRunnerComponent implements OnInit, OnDestroy {

  private $save = new Subject()
  private $finish = new Subject()
  private _unsubscribe$ = new Subject()

  testRun: TestRun
  currentQuestion: QuestionAnswer

  remainingTime$: Observable<string>

  constructor(private runService: RunService,
              private activatedRoute: ActivatedRoute,
              private router: Router) {
  }

  ngOnInit() {
    this.loadSub()
    this.finishSub()

    this.remainingTimeObs()
  }

  private remainingTimeObs() {
    let timeDiffObs = timer(1, 1).pipe(
      takeUntil(this._unsubscribe$),
      filter(() => this.testRun != null),
      distinctUntilChanged(),
      map(() => this.testRun.endsAt.diff(moment.utc()))
    )
    this.remainingTime$ = timeDiffObs.pipe(
      map(remaining =>
        (remaining < 0 || this.testRun.finishedAt != null) ? 'Завершено' : moment.utc(remaining).format('HH:mm:ss')
      )
    )
    this.timeIsUpSub(timeDiffObs)
  }

  private timeIsUpSub(timeDiffObs: Observable<number>) {
    timeDiffObs.pipe(
      takeUntil(this._unsubscribe$),
      takeUntil(this.$finish),
      takeWhile(() => this.testRun.finishedAt == null),
      filter(diff => diff < 0),
      tap(() => this.$finish.next())
    ).subscribe()
  }

  private loadSub() {
    const $params: Observable<number> = this.activatedRoute.params.pipe(
      map(params => +params['id']),
      tap(route => console.log(`ROUTE: ${route}`)),
    )
    const $reload: Observable<number> = this.$save.pipe(
      mergeMap(() => this.save())
    )

    merge($params, $reload)
      .pipe(
        retry(),
        takeUntil(this._unsubscribe$),
        mergeMap(id => this.runService.getTestRun(id)),
        tap(res => this.testRun = res),
        tap(res  => this.updateCurrentQuestionSelection(res.questionAnswers)),
        filter(() => this.currentQuestion.answerCodeSnippet.code === '' || this.currentQuestion.answerCodeSnippet.code == null),
      ).subscribe()
  }

  private updateCurrentQuestionSelection(answers: QuestionAnswer[]) {
    let current = this.currentQuestion
    if (current) {
      current = answers.find(a => a.id === current.id)
    } else {
      current = answers[0]
    }
    this.currentQuestion = current
  }

  private finishSub() {
    this.$finish.pipe(
      retry(),
      takeUntil(this._unsubscribe$),
      concatMap(() => this.finish())
    ).subscribe(() => this.router.navigate(['/result', this.testRun.id]))
  }

  public ngOnDestroy(): void {
    this._unsubscribe$.next()
  }

  private getAnswerUpdates() {
    return this.testRun.questionAnswers.map(a => new TestRunAnswerUpdate(a.id, a.answerCodeSnippet))
  }

  private save(): Observable<number> {
    const updates = this.getAnswerUpdates()
    return this.runService.updateTestRunAnswers(this.testRun.id, updates).pipe(
      map(() => this.testRun.id)
    )
  }

  private finish(): Observable<number> {
    const updates = this.getAnswerUpdates()
    return this.runService.finishTestRun(this.testRun.id, updates).pipe(
      map(() => this.testRun.id)
    )
  }
}
