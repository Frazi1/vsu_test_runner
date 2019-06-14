import { Component, OnInit } from '@angular/core'
import { InstanceService } from '../../../services/instance.service'
import { TestInstance } from '../../../shared/instance/TestInstance'
import { ActivatedRoute, Router } from '@angular/router'
import { TestInstanceUpdate } from '../../../shared/instance/TestInstanceUpdate'
import { TestInstanceAssigneeDto } from '../../../shared/TestInstanceAssigneeDto'
import { switchMap, tap } from 'rxjs/operators'

@Component({
  selector:    'app-test-instance-editor',
  templateUrl: './test-instance-editor.component.html',
  styleUrls:   ['./test-instance-editor.component.scss']
})
export class TestInstanceEditorComponent implements OnInit {

  testInstance: TestInstance
  selectedRange: string

  private paramSubscription


  constructor(private instanceService: InstanceService,
              private router: Router,
              private route: ActivatedRoute) {
  }

  ngOnInit() {
    this.paramSubscription = this.route.params.subscribe(params => {
      const id = params['id']
      if (id) {
        this.instanceService.getTestInstance(+id).subscribe(res => this.testInstance = res)
      }
    })
  }

  private onSelectedRangedValueChange(e, value: string): void {
    const startStr = value[0]
    const endStr = value[1]
    this.testInstance.availableAfter = new Date(startStr)
    this.testInstance.disabledAfter = new Date(endStr)
  }

  private onAssigneesChange(newAssignees: TestInstanceAssigneeDto[]) {
    this.testInstance.assignees = newAssignees
  }

  private getDuration(): string {
    if (!this.testInstance.disabledAfter || !this.testInstance.availableAfter) {
      return null
    }
    // const res: number = (this.test.disabledAfter - this.test.availableAfter) as number;
    // return `${res / 100 / 60} минут`;
  }

  private save(): void {
    const testInstanceUpdate = new TestInstanceUpdate(this.testInstance.availableAfter,
      this.testInstance.disabledAfter,
      this.testInstance.timeLimit,
      this.testInstance.assignees
    )

    this.instanceService.updateTestInstance(this.testInstance.id, testInstanceUpdate).pipe(
      switchMap(() => this.instanceService.getTestInstance(this.testInstance.id)),
      tap(res => this.testInstance = res)
    ).subscribe()
  }
}
