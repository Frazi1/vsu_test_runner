import { CodeSnippet } from '../CodeSnippet'
import { Type } from 'class-transformer'

export class TestingInputGeneratorDto {

  @Type(() => Number)
  id: number = undefined

  @Type(() => String)
  description: string = ''

  @Type(() => CodeSnippet)
  codeSnippet: CodeSnippet


  constructor(codeSnippet: CodeSnippet = null) {
    this.codeSnippet = codeSnippet
  }

  public static EMPTY(): TestingInputGeneratorDto {
    const snippet = CodeSnippet.EMPTY()
    return new TestingInputGeneratorDto(snippet)
  }
}
