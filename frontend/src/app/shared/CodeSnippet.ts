import {CodeLanguage} from './CodeLanguage';
import {JsonObject, JsonProperty} from 'json2typescript';
import {Function} from './Function';

@JsonObject('CodeSnippet')
export class CodeSnippet {

  @JsonProperty('id', Number)
  public id: number;

  @JsonProperty('language', CodeLanguage)
  public language: CodeLanguage;

  private _code: string = undefined;

  @JsonProperty('code', [String])
  get code_array(): string[] {
    return this._code.split('\n');
  }

  set code_array(value: string[]) {
    this._code = value.join('\n');
  }

  get code(): string {
    return this._code;
  }

  set code(value: string) {
    this._code = value;
  }

  @JsonProperty('function', Function)
  public functionObj: Function;

  constructor(id: number = null, language: CodeLanguage = null, code: string[] = [], functionObj: Function) {
    this.id = id;
    this.language = language;
    this.code_array = code;
    this.functionObj = functionObj;
  }
}
