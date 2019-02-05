import {CodeLanguage} from './CodeLanguage';
import {JsonObject, JsonProperty} from 'json2typescript';
import {Function} from './Function';

@JsonObject('CodeSnippet')
export class CodeSnippet {

  @JsonProperty('id', Number)
  public id: number;

  @JsonProperty('language', CodeLanguage)
  public language: CodeLanguage;

  @JsonProperty('code', [String])
  public code: string[];

  @JsonProperty('function', Function)
  public functionObj: Function;

  constructor(id: number = null, language: CodeLanguage = null, code: string[] = [], functionObj: Function) {
    this.id = id;
    this.language = language;
    this.code = code;
    this.functionObj = functionObj;
  }
}
