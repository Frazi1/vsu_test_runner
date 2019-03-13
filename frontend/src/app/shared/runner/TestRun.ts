import { TestRunQuestion } from './TestRunQuestion'
import { Exclude, Type } from 'class-transformer'

export class TestRun {
  id: number = undefined
  name: string = undefined
  timeLimit: number = undefined
  startedAt: Date = undefined
  endsAt: Date = undefined
  @Type(() => TestRunQuestion)
  questionAnswers: TestRunQuestion[] = undefined
  private _finishedAt: Date = undefined

  @Exclude()
  public get isFinished(): boolean {
    return this._finishedAt != null
  }
}
