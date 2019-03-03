import { CodeSnippet } from '../CodeSnippet'
import { Type } from 'class-transformer'


export class TestRunQuestion {
  id: number = undefined
  name: string = undefined
  description: string = undefined
  functionId: number = undefined

  @Type(() => CodeSnippet)
  answerCodeSnippet: CodeSnippet = undefined
}
