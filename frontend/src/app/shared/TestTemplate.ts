import { TestQuestionTemplate } from './TestQuestionTemplate'
import { JsonObject, JsonProperty } from 'json2typescript'

@JsonObject('TestTemplate')
export class TestTemplate {


  @JsonProperty('id', Number)
  private _id: number

  @JsonProperty('isDeleted', Boolean)
  private _isDeleted: boolean = undefined

  @JsonProperty('name', String)
  private _name: string

  @JsonProperty('timeLimit', Number, true)
  private _timeLimit: number

  @JsonProperty('questionTemplates', [TestQuestionTemplate])
  private _questionTemplates: TestQuestionTemplate[]


  // region Getters/Setters
  public get isDeleted(): boolean {
    return this._isDeleted
  }

  public set isDeleted(value: boolean) {
    this._isDeleted = value
  }

  public get id(): number {
    return this._id
  }

  public set id(value: number) {
    this._id = value
  }

  public get name(): string {
    return this._name
  }

  public set name(value: string) {
    this._name = value
  }

  public get timeLimit(): number {
    return this._timeLimit
  }

  public set timeLimit(value: number) {
    this._timeLimit = value
  }

  public get questionTemplates(): TestQuestionTemplate[] {
    return this._questionTemplates
  }

  public set questionTemplates(value: TestQuestionTemplate[]) {
    this._questionTemplates = value
  }

  // endregion

  constructor(id: number                                = null,
              name: string                              = '',
              timeLimit: number                         = null,
              questionTemplates: TestQuestionTemplate[] = []) {
    this._id = id
    this._name = name
    this._timeLimit = timeLimit
    this._questionTemplates = questionTemplates
  }
}
