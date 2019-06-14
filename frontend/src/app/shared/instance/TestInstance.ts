import { QuestionInstance } from './QuestionInstance'
import { Type } from 'class-transformer'
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
  assignees: TestInstanceAssigneeDto[] = undefined
}
