import { QuestionAnswer } from './QuestionAnswer'
import { Exclude, Type } from 'class-transformer'

export class TestRun {
  id: number = undefined
  name: string = undefined
  timeLimit: number = undefined
  startedAt: Date = undefined
  endsAt: Date = undefined
  @Type(() => QuestionAnswer)
  questionAnswers: QuestionAnswer[] = undefined
  private _finishedAt: Date = undefined

  @Exclude()
  public get isFinished(): boolean {
    return this._finishedAt != null
  }
}
