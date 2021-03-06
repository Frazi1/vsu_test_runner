import { CodeSnippet } from '../CodeSnippet'
import { Type } from 'class-transformer'
import { CodeExecutionResponseDto } from './CodeExecutionResponseDto'


export class QuestionAnswer {
  id: number = undefined
  name: string = undefined
  description: string = undefined
  functionId: number = undefined
  validationPassed: boolean
  isValidated: boolean

  @Type(() => CodeExecutionResponseDto)
  iterations: CodeExecutionResponseDto[]

  @Type(() => CodeSnippet)
  answerCodeSnippet: CodeSnippet = undefined
}
