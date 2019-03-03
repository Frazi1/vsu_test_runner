import { TestInstance } from './TestInstance'
import { Type } from 'class-transformer'

export class QuestionInstance {

  id: number = undefined
  name = ''
  timeLimit: number = undefined

  @Type(() => TestInstance)
  tests: TestInstance[] = undefined
}
