import {Component, OnInit} from '@angular/core';
import {RunService} from '../../../services/run.service';
import {ActivatedRoute} from '@angular/router';
import {Subscription} from 'rxjs/index';
import {TestRun} from '../../../shared/runner/TestRun';

@Component({
  selector: 'app-test-runner',
  templateUrl: './test-runner.component.html',
  styleUrls: ['./test-runner.component.less']
})
export class TestRunnerComponent implements OnInit {

  private routeSubscription: Subscription;
  private testRun: TestRun;

  constructor(private runService: RunService,
              private activatedRoute: ActivatedRoute) {
  }

  ngOnInit() {
    this.routeSubscription = this.activatedRoute.params.subscribe(params => {
      const id = +params['id'];
      this.runService.getTestRun(id).subscribe(testRun => this.testRun = testRun);
    });
  }

}
