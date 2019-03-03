import { CodeType } from '../CodeType'
import { Type } from 'class-transformer'

export class DeclarativeInputArgumentItem {

  inputValue: string = undefined
  id: number = undefined
  argumentIndex: number = undefined

  @Type(() => CodeType)
  inputType: CodeType = undefined
}
