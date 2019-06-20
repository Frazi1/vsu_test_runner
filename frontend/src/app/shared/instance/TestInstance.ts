import { QuestionInstance } from './QuestionInstance'
import { Exclude, Expose, Type } from 'class-transformer'
import { TestInstanceAssigneeDto } from '../TestInstanceAssigneeDto'

export class TestInstance {

  id: number = undefined

  name = ''

  createdAt: Date = undefined

  availableAfter: Date = undefined

  disabledAfter: Date = undefined

  timeLimit: number = undefined

  @Type(() => QuestionInstance)
  questions: QuestionInstance[] = undefined

  @Type(() => TestInstanceAssigneeDto)
  userAssignees: TestInstanceAssigneeDto[] = []

  @Type(() => TestInstanceAssigneeDto)
  groupAssignees: TestInstanceAssigneeDto[] = []
}
