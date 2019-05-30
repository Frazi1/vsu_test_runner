import { CodeLanguage } from './CodeLanguage'
import { Function } from './Function'
import { Expose, Type } from 'class-transformer'

export class CodeSnippet {

  id: number

  @Type(() => CodeLanguage)
  language: CodeLanguage

  code: string = undefined

  constructor(id: number = undefined, language: CodeLanguage = undefined, code: string[] = []) {
    this.id = id
    this.language = language
    this.code_array = code
  }

  get code_array(): string[] {
    return this.code.split('\n')
  }

  set code_array(value: string[]) {
    this.code = value.join('\n')
  }

  public static EMPTY(): CodeSnippet {
    return new CodeSnippet(undefined, undefined, [])
  }
}
