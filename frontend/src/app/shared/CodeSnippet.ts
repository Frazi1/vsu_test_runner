import { CodeLanguage } from './CodeLanguage'
import { Function } from './Function'
import { Expose, Type } from 'class-transformer'

export class CodeSnippet {

  id: number

  @Type(() => CodeLanguage)
  language: CodeLanguage

  code: string = undefined

  @Expose({name: 'function'})
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

  public static EMPTY(): CodeSnippet {
    const functionObj = new Function()
    return new CodeSnippet(null, null, [], functionObj)
  }
}
