import { CodeLanguage } from '../CodeLanguage'
import { Exclude, Expose, Type } from 'class-transformer'
import { ScaffoldingType } from '../ScaffoldingType'


export class CodeSnippetScaffoldingDto {

  @Type(() => CodeLanguage)
  codeLanguage: CodeLanguage = undefined

  code: string = undefined

  @Exclude() private _scaffoldingType: ScaffoldingType

  @Expose()
  public get scaffoldingType(): string {
    return ScaffoldingType[this._scaffoldingType]
  }

  public set scaffoldingType(value: string) {
    this._scaffoldingType = ScaffoldingType[value]
  }
}
