import { JsonObject, JsonProperty } from 'json2typescript'
import { Function } from '../Function'
import { CodeLanguage } from '../CodeLanguage'

@JsonObject('FunctionScaffoldingDto')
export class FunctionScaffoldingDto {
  @JsonProperty('function', Function)
  private _function: Function = undefined

  @JsonProperty('language', CodeLanguage)
  private _codeLanguage: CodeLanguage = undefined

  @JsonProperty('code')
  private _code: string = undefined


  // region Getters
  get functionObj(): Function {
    return this._function
  }

  get codeLanguage(): CodeLanguage {
    return this._codeLanguage
  }

  get code(): string {
    return this._code
  }

  // endregion
}
