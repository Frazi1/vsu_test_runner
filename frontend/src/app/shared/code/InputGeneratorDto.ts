import { CodeSnippet } from '../CodeSnippet'
import { Type } from 'class-transformer'
import { GeneratorCallArgumentDto } from './GeneratorCallArgumentDto'

export class InputGeneratorDto {

  @Type(() => Number)
  id: number = undefined

  name: string

  @Type(() => String)
  description: string = ''

  @Type(() => CodeSnippet)
  codeSnippet: CodeSnippet

  @Type(() => GeneratorCallArgumentDto)
  callArguments: GeneratorCallArgumentDto[]


  constructor(codeSnippet: CodeSnippet = null) {
    this.codeSnippet = codeSnippet
  }

  public static EMPTY(): InputGeneratorDto {
    const snippet = CodeSnippet.EMPTY()
    return new InputGeneratorDto(snippet)
  }
}
