import { CodeSnippet } from '../CodeSnippet'
import { Type } from 'class-transformer'


export class QuestionAnswer {
  id: number = undefined
  name: string = undefined
  description: string = undefined
  functionId: number = undefined
  validationPassed: boolean
  isValidated: boolean

  @Type(() => CodeSnippet)
  answerCodeSnippet: CodeSnippet = undefined
}
