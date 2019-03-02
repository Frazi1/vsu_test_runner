import { JsonObject, JsonProperty } from 'json2typescript'

@JsonObject('TestInstanceUpdate')
export class TestInstanceUpdate {
  @JsonProperty('availableAfter')
  private _availableAfter: Date = undefined

  @JsonProperty('disabledAfter')
  private _disabledAfter: Date = undefined

  @JsonProperty('timeLimit')
  private _timeLimit: number = undefined

  constructor(availableAfter: Date, disabledAfter: Date, timeLimit: number) {
    this.availableAfter = availableAfter
    this.disabledAfter = disabledAfter
    this.timeLimit = timeLimit
  }

  // region Getters/Setters
  get availableAfter(): Date {
    return this._availableAfter
  }

  set availableAfter(value: Date) {
    this._availableAfter = value
  }

  get disabledAfter(): Date {
    return this._disabledAfter
  }

  set disabledAfter(value: Date) {
    this._disabledAfter = value
  }

  get timeLimit(): number {
    return this._timeLimit
  }

  set timeLimit(value: number) {
    this._timeLimit = value
  }

  // endregion
}
