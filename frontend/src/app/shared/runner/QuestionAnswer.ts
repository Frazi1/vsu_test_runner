import { CodeSnippet } from '../CodeSnippet'
import { Type } from 'class-transformer'
import { CodeRunIterationDto } from './CodeRunIterationDto'


export class QuestionAnswer {
  id: number = undefined
  name: string = undefined
  description: string = undefined
  functionId: number = undefined
  validationPassed: boolean
  isValidated: boolean

  @Type(() => CodeRunIterationDto)
  iterations: CodeRunIterationDto[]

  @Type(() => CodeSnippet)
  answerCodeSnippet: CodeSnippet = undefined
}
