import { CodeLanguage } from '../CodeLanguage'
import { JsonObject, JsonProperty } from 'json2typescript'
import { CodeType } from '../CodeType'

@JsonObject('CodeExecutionResult')
export class CodeExecutionResult {

  @JsonProperty('language', CodeLanguage)
  private _language: CodeLanguage = undefined

  @JsonProperty('output', String)
  private _output: string = undefined

  @JsonProperty('outputType', CodeType)
  private _outputType: CodeType = undefined

  @JsonProperty('error', String)
  private _error: string = undefined


  // region Getters
  get language(): CodeLanguage {
    return this._language
  }

  get output(): string {
    return this._output
  }

  get outputType(): CodeType {
    return this._outputType
  }

  get error(): string {
    return this._error
  }

  // endregion
}
