import { TestInstance } from './TestInstance';
import { JsonObject, JsonProperty } from 'json2typescript';

@JsonObject('QuestionInstance')
export class QuestionInstance {

  @JsonProperty('id')
  private _id: number = undefined;

  @JsonProperty('name')
  private _name = '';

  @JsonProperty('timeLimit')
  private _timeLimit: number = undefined;

  @JsonProperty('tests')
  private _tests: TestInstance[] = undefined;


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

  get timeLimit(): number {
    return this._timeLimit;
  }

  set timeLimit(value: number) {
    this._timeLimit = value;
  }

  get tests(): TestInstance[] {
    return this._tests;
  }

  set tests(value: TestInstance[]) {
    this._tests = value;
  }

  // endregion
}
