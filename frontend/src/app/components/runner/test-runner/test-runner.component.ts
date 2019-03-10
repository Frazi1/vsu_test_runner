import { Component, OnInit } from '@angular/core'
import { RunService } from '../../../services/run.service'
import { ActivatedRoute } from '@angular/router'
import { merge, Observable, Subject, Subscription } from 'rxjs'
import { TestRun } from '../../../shared/runner/TestRun'
import { TestRunQuestion } from '../../../shared/runner/TestRunQuestion'
import { TestRunAnswerUpdate } from '../../../shared/runner/TestRunAnswerUpdate'
import { map, mergeMap, retry, tap } from 'rxjs/internal/operators'

@Component({
  selector:    'app-test-runner',
  templateUrl: './test-runner.component.html',
  styleUrls:   ['./test-runner.component.less']
})
export class TestRunnerComponent implements OnInit {

  private $save = new Subject()
  private $finish = new Subject()

  private subscription: Subscription
  private _testRun: TestRun
  private _currentQuestionIndex = 0

  constructor(private runService: RunService,
              private activatedRoute: ActivatedRoute) {
  }

  get currentQuestion(): TestRunQuestion {
    return this._testRun.questionAnswers[this._currentQuestionIndex]
  }

  ngOnInit() {
    const $params: Observable<number> = this.activatedRoute.params.pipe(
      map(params => +params['id']),
      tap(route => console.log(`ROUTE: ${route}`))
    )
    const $reload: Observable<number> = this.$save.pipe(
      mergeMap(_ => this.save())
    )

    this.subscription = merge($params, $reload, this.$finish.pipe(mergeMap(_ => this.finish())))
      .pipe(
        retry(),
        mergeMap(id => this.runService.getTestRun(id)),
        tap(res => this._testRun = res)
      ).subscribe()
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
