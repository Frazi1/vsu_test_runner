import { Component, OnInit } from '@angular/core'
import { TestRun } from '../../../shared/runner/TestRun'
import { RunService } from '../../../services/run.service'
import { Router } from '@angular/router'

@Component({
  selector:    'app-test-runs-list',
  templateUrl: './test-runs-list.component.html',
  styleUrls:   ['./test-runs-list.component.scss']
})
export class TestRunsListComponent implements OnInit {

  _testRuns: TestRun[]

  constructor(private runService: RunService,
              private router: Router) {
  }

  async ngOnInit() {
    this._testRuns = await this.runService.getActiveTestRuns().toPromise()
  }

  private openTestRun(id: number): void {
    this.router.navigate(['run', id])
  }
}
