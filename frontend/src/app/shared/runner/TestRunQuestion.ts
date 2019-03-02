import { JsonObject, JsonProperty } from 'json2typescript'
import { CodeSnippet } from '../CodeSnippet'

@JsonObject('TestRunQuestion')
export class TestRunQuestion {

  @JsonProperty('id')
  private _id: number = undefined

  @JsonProperty('name')
  private _name: string = undefined

  @JsonProperty('description')
  private _description: string = undefined

  @JsonProperty('functionId')
  private _functionId: number = undefined

  @JsonProperty('answerCodeSnippet', CodeSnippet)
  private _answerCodeSnippet: CodeSnippet = undefined

  // region Getters/Setters
  get id(): number {
    return this._id
  }

  get name(): string {
    return this._name
  }

  get description(): string {
    return this._description
  }

  get answerCodeSnippet(): CodeSnippet {
    return this._answerCodeSnippet
  }

  set answerCodeSnippet(value: CodeSnippet) {
    this._answerCodeSnippet = value
  }

  get functionId(): number {
    return this._functionId
  }

// endregion
}
