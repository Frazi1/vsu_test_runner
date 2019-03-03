import { CodeType } from './CodeType'
import { Type } from 'class-transformer'


export class FunctionArgument {
  name: string

  @Type(() => CodeType)
  type: CodeType


  constructor(name: string, type: CodeType) {
    this.name = name
    this.type = type
  }
}
