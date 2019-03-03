import { TestRunQuestion } from './TestRunQuestion'
import { Type } from 'class-transformer'

export class TestRun {
  id: number = undefined
  name: string = undefined
  timeLimit: number = undefined
  startedAt: Date = undefined
  finishedAt: Date = undefined
  endsAt: Date = undefined

  @Type(() => TestRunQuestion)
  questionAnswers: TestRunQuestion[] = undefined

}
