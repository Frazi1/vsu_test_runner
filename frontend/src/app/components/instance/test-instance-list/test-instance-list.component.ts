import { Component, OnInit } from '@angular/core'
import { InstanceService } from '../../../services/instance.service'
import { TestInstance } from '../../../shared/instance/TestInstance'
import { RunService } from '../../../services/run.service'
import { tap } from 'rxjs/internal/operators'

@Component({
  selector:    'app-test-instance-list',
  templateUrl: './test-instance-list.component.html',
  styleUrls:   ['./test-instance-list.component.less']
})
export class TestInstanceListComponent implements OnInit {

  private tests: TestInstance[]

  constructor(private instanceService: InstanceService,
              private runService: RunService) {
  }

  ngOnInit() {
    this.instanceService.getTestInstances()
        .subscribe(res => this.tests = res)
  }

  startTest(test: TestInstance) {
    this.runService.startRunFromInstance(test.id)
        .pipe(
          tap(res => console.log(`Run started: ${res}`))
        )
        .subscribe()
  }
}
