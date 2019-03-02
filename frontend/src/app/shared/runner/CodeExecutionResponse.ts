import { JsonObject, JsonProperty } from 'json2typescript';
import { CodeExecutionResult } from './CodeRunResult';

@JsonObject('CodeExecutionResponse')
export class CodeExecutionResponse {

  @JsonProperty('clientId', String)
  private _clientId: string = undefined;

  @JsonProperty('codeRunResult', CodeExecutionResult)
  private _codeRunResult: CodeExecutionResult = undefined;


  // region Getters
  get clientId(): string {
    return this._clientId;
  }

  get codeRunResult(): CodeExecutionResult {
    return this._codeRunResult;
  }

  // endregion
}
