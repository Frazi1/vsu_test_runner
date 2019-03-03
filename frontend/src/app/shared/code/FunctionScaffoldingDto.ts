import { Function } from '../Function'
import { CodeLanguage } from '../CodeLanguage'
import { Expose, Type } from 'class-transformer'


export class FunctionScaffoldingDto {

  @Type(() => Function)
  @Expose({name: 'function'})
  functionObj: Function = undefined

  @Type(() => CodeLanguage)
  codeLanguage: CodeLanguage = undefined

  code: string = undefined

  // endregion
}
