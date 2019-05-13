import { Component, OnDestroy, OnInit } from '@angular/core'
import { RunService } from '../../../services/run.service'
import { ActivatedRoute, Router } from '@angular/router'
import { merge, Observable, Subject, Subscription } from 'rxjs'
import { TestRun } from '../../../shared/runner/TestRun'
import { QuestionAnswer } from '../../../shared/runner/QuestionAnswer'
import { TestRunAnswerUpdate } from '../../../shared/runner/TestRunAnswerUpdate'
import { concatMap, filter, map, mergeMap, retry, take, takeUntil, tap, } from 'rxjs/internal/operators'
import { CodeService } from '../../../services/code.service'

@Component({
  selector:    'app-test-runner',
  templateUrl: './test-runner.component.html',
  styleUrls:   ['./test-runner.component.less']
})
export class TestRunnerComponent implements OnInit, OnDestroy {

  private $save = new Subject()
  private $finish = new Subject()
  private _unsubscribe$ = new Subject()

  private _testRun: TestRun
  private _currentQuestionIndex = 0
  private _currentId: number

  constructor(private runService: RunService,
              private activatedRoute: ActivatedRoute,
              private router: Router,
              private codeService: CodeService) {
  }

  get currentQuestion(): QuestionAnswer {
    return this._testRun.questionAnswers[this._currentQuestionIndex]
  }

  ngOnInit() {
    const $params: Observable<number> = this.activatedRoute.params.pipe(
      map(params => +params['id']),
      tap(route => console.log(`ROUTE: ${route}`)),
      tap(id => this._currentId = id)
    )
    const $reload: Observable<number> = this.$save.pipe(
      mergeMap(() => this.save())
    )

    merge($params, $reload)
      .pipe(
        retry(),
        takeUntil(this._unsubscribe$),
        mergeMap(id => this.runService.getTestRun(id)),
        tap(res => this._testRun = res),
        filter(
          _ => this.currentQuestion.answerCodeSnippet.code === '' || this.currentQuestion.answerCodeSnippet.code == null),
        // mergeMap(_ => this.codeService.scaffoldFunction(this.currentQuestion.functionId,
        //   this.currentQuestion.answerCodeSnippet.language, ScaffoldingType.FUNCTION_ONLY
        //   )
        // ),
        // tap(functionScaffolding => this.currentQuestion.answerCodeSnippet.code = functionScaffolding.code)
      ).subscribe()

    this.$finish.pipe(
      retry(),
      takeUntil(this._unsubscribe$),
      concatMap(() => this.finish())
    ).subscribe(() => this.router.navigate(['/result', this._currentId]))
  }

  public ngOnDestroy(): void {
    this._unsubscribe$.next()
  }

  private nextQuestion(): void {
    if (this._currentQuestionIndex < this._testRun.questionAnswers.length - 1) {
      this._currentQuestionIndex++
    }
  }

  private previousQuestion(): void {
    if (this._currentQuestionIndex > 0) {
      this._currentQuestionIndex--
    }
  }

  private getAnswerUpdates() {
    return this._testRun.questionAnswers.map(a => new TestRunAnswerUpdate(a.id, a.answerCodeSnippet))
  }

  private save(): Observable<number> {
    const updates = this.getAnswerUpdates()
    return this.runService.updateTestRunAnswers(this._testRun.id, updates)
  }

  private finish(): Observable<number> {
    const updates = this.getAnswerUpdates()
    return this.runService.finishTestRun(this._testRun.id, updates)
  }
}
