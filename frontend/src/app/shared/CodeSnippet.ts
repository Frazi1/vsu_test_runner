import {CodeLanguage} from './CodeLanguage';
import {JsonObject, JsonProperty} from 'json2typescript';

@JsonObject('CodeSnippet')
export class CodeSnippet {

  @JsonProperty('id', Number)
  public id: number;

  @JsonProperty('language', CodeLanguage)
  public language: CodeLanguage;

  @JsonProperty('code', [String])
  public code: string[];


  constructor(id: number = null, language: CodeLanguage = null, code: string[] = []) {
    this.id = id;
    this.language = language;
    this.code = code;
  }
}
