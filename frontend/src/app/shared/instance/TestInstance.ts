import { JsonObject, JsonProperty } from 'json2typescript'
import { QuestionInstance } from './QuestionInstance'

@JsonObject('TestInstance')
export class TestInstance {
  @JsonProperty('id')
  private _id: number = undefined

  @JsonProperty('name')
  private _name = ''

  @JsonProperty('createdAt')
  private _createdAt: Date = undefined

  @JsonProperty('availableAfter')
  private _availableAfter: Date = undefined

  @JsonProperty('disabledAfter')
  private _disabledAfter: Date = undefined

  @JsonProperty('timeLimit')
  private _timeLimit: number = undefined

  @JsonProperty('questions')
  private _questions: QuestionInstance[] = undefined


  // region Getters/Setters
  get id(): number {
    return this._id
  }

  set id(value: number) {
    this._id = value
  }

  get name(): string {
    return this._name
  }

  set name(value: string) {
    this._name = value
  }

  get createdAt(): Date {
    return this._createdAt
  }

  set createdAt(value: Date) {
    this._createdAt = value
  }

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

  get questions(): QuestionInstance[] {
    return this._questions
  }

  set questions(value: QuestionInstance[]) {
    this._questions = value
  }

  // endregion
}
