import { CodeSnippet } from './CodeSnippet'
import { Type } from 'class-transformer'


export class TestQuestionTemplate {

  name: string

  description: string

  timeLimit: number


  @Type(() => CodeSnippet)
  codeSnippet: CodeSnippet

  constructor(name: string             = '',
              text: string             = '',
              timeLimit: number        = null,
              codeSnippet: CodeSnippet = null) {
    this.name = name
    this.description = text
    this.timeLimit = timeLimit
    this.codeSnippet = codeSnippet
  }
}
