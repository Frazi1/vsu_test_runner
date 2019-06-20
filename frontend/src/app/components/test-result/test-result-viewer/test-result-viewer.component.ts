import { Component, OnDestroy, OnInit } from '@angular/core'
import { TestRun } from '../../../shared/runner/TestRun'
import { FinishedRunService } from '../../../services/finished-run.service'
import { Subject, Subscription } from 'rxjs'
import { map, mergeMap, takeUntil, tap } from 'rxjs/operators'
import { ActivatedRoute, Router } from '@angular/router'
import { QuestionState } from '../../../shared/question-state.enum'
import { QuestionAnswer } from '../../../shared/runner/QuestionAnswer'
import { BaseComponent } from '../../base.component'

@Component({
  selector:    'app-test-result-viewer',
  templateUrl: './test-result-viewer.component.html',
  styleUrls:   ['./test-result-viewer.component.scss']
})
export class TestResultViewerComponent extends BaseComponent implements OnInit, OnDestroy {

  QuestionState = QuestionState

  private $answerLink = new Subject<number>()

  private subscription: Subscription
  private testRun: TestRun

  currentQuestion: QuestionAnswer

  constructor(private finishedRunService: FinishedRunService,
              private route: ActivatedRoute,
              private router: Router) {
    super()
  }

  ngOnInit() {
    this.subscription = this.route.params.pipe(
      takeUntil(this.onDestroy$),
      map(params => +params['id']),
      mergeMap(id => this.finishedRunService.getFinishedRun(id)),
      tap(run => this.testRun = run),
      tap(run => this.currentQuestion = run.questionAnswers[0])
    ).subscribe()
  }

  public get answersCount(): number {
    return this.testRun.questionAnswers.length
  }

  public get correctAnswersCount(): number {
    return this.testRun.questionAnswers.filter(a => a.validationPassed).length
  }
}
