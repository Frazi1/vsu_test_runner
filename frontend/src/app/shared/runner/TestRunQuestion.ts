import {JsonObject, JsonProperty} from 'json2typescript';
import {CodeSnippet} from '../CodeSnippet';

@JsonObject('TestRunQuestion')
export class TestRunQuestion {

  @JsonProperty('id')
  private _id: number = undefined;

  @JsonProperty('name')
  private _name: string = undefined;

  @JsonProperty('description')
  private _description: string = undefined;

  @JsonProperty('answerCodeSnippet', CodeSnippet)
  private _answerCodeSnippet: CodeSnippet = undefined;

  // region Getters/Setters
  get id(): number {
    return this._id;
  }

  set id(value: number) {
    this._id = value;
  }

  get name(): string {
    return this._name;
  }

  set name(value: string) {
    this._name = value;
  }

  get description(): string {
    return this._description;
  }

  set description(value: string) {
    this._description = value;
  }

  get answerCodeSnippet(): CodeSnippet {
    return this._answerCodeSnippet;
  }

  set answerCodeSnippet(value: CodeSnippet) {
    this._answerCodeSnippet = value;
  }

  // endregion
}
