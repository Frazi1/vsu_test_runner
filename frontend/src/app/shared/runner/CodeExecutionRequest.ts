import { JsonObject, JsonProperty } from 'json2typescript';
import { CodeType } from '../CodeType';
import { CodeLanguage } from '../CodeLanguage';

@JsonObject('CodeExecutionRequest')
export class CodeExecutionRequest {

  @JsonProperty('clientId', String)
  private _clientId: string = undefined;

  @JsonProperty('returnType', CodeType)
  private _returnType: CodeType = undefined;

  @JsonProperty('functionId', Number)
  private _functionId: number = undefined;

  @JsonProperty('language', CodeLanguage)
  private _language: CodeLanguage = undefined;

  @JsonProperty('code', String)
  private _code: string = undefined;

  @JsonProperty('isPlainCode', Boolean)
  private _isPlainCode: boolean = undefined;


  private constructor(clientId: string, returnType: CodeType, functionId: number, language: CodeLanguage, code: string,
                      isPlainCode: boolean) {
    this._clientId = clientId;
    this._returnType = returnType;
    this._functionId = functionId;
    this._language = language;
    this._code = code;
    this._isPlainCode = isPlainCode;
  }

  public static fromReturnType(language: CodeLanguage, code: string, returnType: CodeType, isPlainCode: boolean,
                               clientId: string = null): CodeExecutionRequest {
    return new CodeExecutionRequest(clientId, returnType, null, language, code, isPlainCode);
  }

  public static fromFunctionId(language: CodeLanguage, code: string, functionId: number, isPlainCode: boolean,
                               clientId: string = null): CodeExecutionRequest {
    return new CodeExecutionRequest(clientId, null, functionId, language, code, isPlainCode);
  }


// region Getters/Setters
  get clientId(): string {
    return this._clientId;
  }

  set clientId(value: string) {
    this._clientId = value;
  }

  get returnType(): CodeType {
    return this._returnType;
  }

  set returnType(value: CodeType) {
    this._returnType = value;
  }

  get functionId(): number {
    return this._functionId;
  }

  set functionId(value: number) {
    this._functionId = value;
  }

  get language(): CodeLanguage {
    return this._language;
  }

  set language(value: CodeLanguage) {
    this._language = value;
  }

  get code(): string {
    return this._code;
  }

  set code(value: string) {
    this._code = value;
  }

  // endregion
}
