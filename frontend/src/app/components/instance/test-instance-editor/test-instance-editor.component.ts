import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {InstanceService} from '../../../services/instance.service';
import {TestInstance} from '../../../shared/instance/TestInstance';
import {ActivatedRoute, Router} from '@angular/router';

@Component({
  selector: 'app-test-instance-editor',
  templateUrl: './test-instance-editor.component.html',
  styleUrls: ['./test-instance-editor.component.less']
})
export class TestInstanceEditorComponent implements OnInit {
  private test: TestInstance;
  private paramSubscription;

  private selectedRange: string;

  constructor(private instanceService: InstanceService,
              private router: Router,
              private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.paramSubscription = this.route.params.subscribe(params => {
      const id = params['id'];
      if (id) {
        this.instanceService.getTestInstance(+id).subscribe(res => this.test = res);
      }
    });
  }

  private onSelectedRangedValueChange(e, value: string): void {
    const startStr = value[0];
    const endStr = value[1];
    this.test.availableAfter = new Date(startStr);
    this.test.disabledAfter = new Date(endStr);
  }

  private getDuration(): string {
    if (!this.test.disabledAfter || !this.test.availableAfter) {
      return null;
    }
    const res = this.test.disabledAfter - this.test.availableAfter;
    return `${res / 100 / 60} минут`;
  }
}
