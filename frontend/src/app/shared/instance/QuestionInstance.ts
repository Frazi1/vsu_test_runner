import { TestInstance } from './TestInstance'
import { Type } from 'class-transformer'
import { IQuestion } from '../IQuestion'

export class QuestionInstance implements IQuestion {

  id: number = undefined
  name = ''
  timeLimit: number = undefined

  @Type(() => TestInstance)
  tests: TestInstance[] = undefined
}
