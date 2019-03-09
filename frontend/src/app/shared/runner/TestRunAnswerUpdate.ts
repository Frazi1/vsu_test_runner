import { CodeSnippet } from '../CodeSnippet'
import { Type } from 'class-transformer'

export class TestRunAnswerUpdate {

  answerId: number

  @Type(() => CodeSnippet)
  answerCodeSnippet: CodeSnippet


  constructor(questionId: number = null, answerCodeSnippet: CodeSnippet = null) {
    this.answerId = questionId
    this.answerCodeSnippet = answerCodeSnippet
  }
}
