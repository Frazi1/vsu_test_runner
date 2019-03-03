import { CodeLanguage } from '../CodeLanguage'
import { CodeType } from '../CodeType'
import { Type } from 'class-transformer'


export class CodeExecutionResult {

  @Type(() => CodeLanguage)
  language: CodeLanguage = undefined

  output: string = undefined

  @Type(() => CodeType)
  outputType: CodeType = undefined

  error: string = undefined

}
