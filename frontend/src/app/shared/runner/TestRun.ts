import { TestRunQuestion } from './TestRunQuestion';
import { JsonObject, JsonProperty } from 'json2typescript';

@JsonObject('TestRun')
export class TestRun {

  @JsonProperty('id')
  private _id: number = undefined;

  @JsonProperty('name')
  private _name: string = undefined;

  @JsonProperty('timeLimit')
  private _timeLimit: number = undefined;

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

  get startedAt(): Date {
    return this._startedAt;
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

  get questionAnswers(): TestRunQuestion[] {
    return this._questionAnswers;
  }

  get name(): string {
    return this._name;
  }

  get timeLimit(): number {
    return this._timeLimit;
  }

// endregion
}
