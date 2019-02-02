import {Component, OnInit} from '@angular/core';
import {InstanceService} from '../../../services/instance.service';
import {TestInstance} from '../../../shared/instance/TestInstance';

@Component({
  selector: 'app-test-instance-list',
  templateUrl: './test-instance-list.component.html',
  styleUrls: ['./test-instance-list.component.less']
})
export class TestInstanceListComponent implements OnInit {

  private tests: TestInstance[];

  constructor(private instanceService: InstanceService) {
  }

  ngOnInit() {
    this.instanceService.getTestInstances()
      .subscribe(res => this.tests = res);
  }
}
