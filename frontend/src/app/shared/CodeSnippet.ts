import { CodeLanguage } from './CodeLanguage'
import { Function } from './Function'
import { Type } from 'class-transformer'

export class CodeSnippet {

  id: number

  @Type(() => CodeLanguage)
  language: CodeLanguage

  code: string = undefined

  @Type(() => Function)
  functionObj: Function

  constructor(id: number = null, language: CodeLanguage = null, code: string[] = [], functionObj: Function) {
    this.id = id
    this.language = language
    this.code_array = code
    this.functionObj = functionObj
  }

  get code_array(): string[] {
    return this.code.split('\n')
  }

  set code_array(value: string[]) {
    this.code = value.join('\n')
  }
}
