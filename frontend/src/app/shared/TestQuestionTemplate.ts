import {JsonObject, JsonProperty} from 'json2typescript';
import {CodeSnippet} from './CodeSnippet';

@JsonObject('TestQuestionTemplate')
export class TestQuestionTemplate {
  @JsonProperty('name', String)
  public name: string;

  @JsonProperty('description', String)
  public description: string;

  @JsonProperty('timeLimit', String, true)
  public timeLimit: number;

  @JsonProperty('codeSnippet', CodeSnippet)
  private _codeSnippet: CodeSnippet;


  // region Getters/Setters
  get codeSnippet(): CodeSnippet {
    return this._codeSnippet;
  }

  set codeSnippet(value: CodeSnippet) {
    this._codeSnippet = value;
  }

  // endregion

  constructor(name: string = '',
              text: string = '',
              timeLimit: number = null,
              codeSnippet: CodeSnippet = null) {
    this.name = name;
    this.description = text;
    this.timeLimit = timeLimit;
    this.codeSnippet = codeSnippet;
  }
}
