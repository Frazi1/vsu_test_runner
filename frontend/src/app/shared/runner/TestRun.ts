import {TestRunQuestion} from './TestRunQuestion';
import {JsonObject, JsonProperty} from 'json2typescript';

@JsonObject('TestRun')
export class TestRun {

  @JsonProperty('id')
  private _id: number = undefined;

  @JsonProperty('startedAt')
  private _startedAt: Date = undefined;

  @JsonProperty('finishedAt')
  private _finishedAt: Date = undefined;

  @JsonProperty('endsAt')
  private _endsAt: Date = undefined;

  @JsonProperty('questionAnswers', [TestRunQuestion])
  private _questionAnswers: TestRunQuestion[] = undefined;

  // region Getters/Setters
  get id(): number {
    return this._id;
  }

  set id(value: number) {
    this._id = value;
  }

  get startedAt(): Date {
    return this._startedAt;
  }

  set startedAt(value: Date) {
    this._startedAt = value;
  }

  get finishedAt(): Date {
    return this._finishedAt;
  }

  set finishedAt(value: Date) {
    this._finishedAt = value;
  }

  get endsAt(): Date {
    return this._endsAt;
  }

  set endsAt(value: Date) {
    this._endsAt = value;
  }

  get questionAnswers(): TestRunQuestion[] {
    return this._questionAnswers;
  }

  set questionAnswers(value: TestRunQuestion[]) {
    this._questionAnswers = value;
  }

  // endregion
}
