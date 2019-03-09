import { Component, OnInit } from '@angular/core'
import { RunService } from '../../../services/run.service'
import { ActivatedRoute } from '@angular/router'
import { Subscription } from 'rxjs/index'
import { TestRun } from '../../../shared/runner/TestRun'
import { TestRunQuestion } from '../../../shared/runner/TestRunQuestion'
import { TestRunAnswerUpdate } from '../../../shared/runner/TestRunAnswerUpdate'

@Component({
  selector:    'app-test-runner',
  templateUrl: './test-runner.component.html',
  styleUrls:   ['./test-runner.component.less']
})
export class TestRunnerComponent implements OnInit {

  private routeSubscription: Subscription
  private _testRun: TestRun
  private _currentQuestionIndex = 0

  constructor(private runService: RunService,
              private activatedRoute: ActivatedRoute) {
  }

  ngOnInit() {
    this.routeSubscription = this.activatedRoute.params.subscribe(params => {
      const id = +params['id']
      this.runService.getTestRun(id).subscribe(testRun => this._testRun = testRun)
    })
  }

  get currentQuestion(): TestRunQuestion {
    return this._testRun.questionAnswers[this._currentQuestionIndex]
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

  private save(): void {
    const updates = this._testRun.questionAnswers.map(a => new TestRunAnswerUpdate(a.id, a.answerCodeSnippet))
    this.runService.updateTestRunAnswers(this._testRun.id, updates)
        .subscribe(res => this._testRun = res)
  }
}
