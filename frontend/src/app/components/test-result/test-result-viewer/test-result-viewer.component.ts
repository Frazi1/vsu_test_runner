import { Component, OnDestroy, OnInit } from '@angular/core'
import { TestRun } from '../../../shared/runner/TestRun'
import { FinishedRunService } from '../../../services/finished-run.service'
import { Subject, Subscription } from 'rxjs'
import { map, mergeMap, tap } from 'rxjs/operators'
import { ActivatedRoute } from '@angular/router'
import { QuestionState } from '../../../shared/question-state.enum'

@Component({
  selector:    'app-test-result-viewer',
  templateUrl: './test-result-viewer.component.html',
  styleUrls:   ['./test-result-viewer.component.less']
})
export class TestResultViewerComponent implements OnInit, OnDestroy {

  QuestionState = QuestionState

  private $answerLink = new Subject<number>()

  private subscription: Subscription
  private testRun: TestRun
  private currentQuestionIndex = 0

  constructor(private finishedRunService: FinishedRunService,
              private route: ActivatedRoute) { }

  ngOnInit() {
    this.$answerLink.pipe(
      tap(id => this.currentQuestionIndex = id)
    ).subscribe()

    this.subscription = this.route.params.pipe(
      map(params => +params['id']),
      mergeMap(id => this.finishedRunService.getFinishedRun(id)),
      tap(run => this.testRun = run)
    ).subscribe()
  }

  public ngOnDestroy(): void {
    this.subscription.unsubscribe()
  }
}
