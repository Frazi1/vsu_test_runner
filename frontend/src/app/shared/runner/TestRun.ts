import { QuestionAnswer } from './QuestionAnswer'
import { Exclude, Transform, Type } from 'class-transformer'
import * as moment from 'moment'
import { Moment } from 'moment'

export class TestRun {
  id: number = undefined
  name: string = undefined
  timeLimit: number = undefined

  @Type(() => Date)
  @Transform(value => moment.utc(value), {toClassOnly: true})
  startedAt: Date = undefined

  @Type(() => String)
  @Transform(value => moment.utc(value), {toClassOnly: true})
  endsAt: Moment = undefined

  @Type(() => QuestionAnswer)
  questionAnswers: QuestionAnswer[] = undefined

  @Type(() => Date)
  @Transform(value => moment.utc(value), {toClassOnly: true})
  finishedAt: Date = undefined

  @Exclude()
  public get isFinished(): boolean {
    return this.finishedAt != null
  }
}
