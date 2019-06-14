import { TestInstanceAssigneeDto } from '../TestInstanceAssigneeDto'

export class TestInstanceUpdate {

  availableAfter: Date = undefined
  disabledAfter: Date = undefined
  timeLimit: number = undefined
  assignees: TestInstanceAssigneeDto[]

  constructor(availableAfter: Date, disabledAfter: Date, timeLimit: number, assignees: TestInstanceAssigneeDto[]) {
    this.availableAfter = availableAfter
    this.disabledAfter = disabledAfter
    this.timeLimit = timeLimit
    this.assignees = assignees
  }
}
