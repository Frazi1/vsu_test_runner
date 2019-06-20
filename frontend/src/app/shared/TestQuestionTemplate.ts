import { CodeSnippet } from './CodeSnippet'
import { Type } from 'class-transformer'
import { TestingInputDto } from './input/FunctionInputDto'
import { IQuestion } from './IQuestion'


export class TestQuestionTemplate implements IQuestion {
  id: number
  name: string

  description: string

  timeLimit: number


  @Type(() => CodeSnippet)
  codeSnippet: CodeSnippet

  testingInputs: TestingInputDto[]

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
