import { QuestionInstance } from './QuestionInstance'
import { Type } from 'class-transformer'

export class TestInstance {

  id: number = undefined

  name = ''

  createdAt: Date = undefined

  availableAfter: Date = undefined

  disabledAfter: Date = undefined

  timeLimit: number = undefined

  @Type(() => QuestionInstance)
  questions: QuestionInstance[] = undefined
}
