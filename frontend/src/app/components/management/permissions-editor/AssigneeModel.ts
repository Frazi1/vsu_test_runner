import { TestInstanceAssigneeDto } from '../../../shared/TestInstanceAssigneeDto'

export class AssigneeModel {
  assigneeDto: TestInstanceAssigneeDto
  isSelected: boolean


  constructor(assigneeDto: TestInstanceAssigneeDto, isSelected: boolean) {
    this.assigneeDto = assigneeDto
    this.isSelected = isSelected
  }
}


