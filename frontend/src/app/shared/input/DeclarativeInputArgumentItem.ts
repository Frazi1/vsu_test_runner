import {JsonObject, JsonProperty} from 'json2typescript';
import {CodeType} from '../CodeType';

@JsonObject('DeclarativeInputArgumentItem')
export class DeclarativeInputArgumentItem {
  private _id: number = undefined;
  private _argumentIndex: number = undefined;
  private _inputType: CodeType = undefined;
  private _inputValue: string = undefined;


  // region Getters/Setters
  @JsonProperty('id', Number)
  get id(): number {
    return this._id;
  }

  set id(value: number) {
    this._id = value;
  }

  @JsonProperty('argumentIndex', Number)
  get argumentIndex(): number {
    return this._argumentIndex;
  }

  set argumentIndex(value: number) {
    this._argumentIndex = value;
  }

  @JsonProperty('inputType', CodeType)
  get inputType(): CodeType {
    return this._inputType;
  }

  set inputType(value: CodeType) {
    this._inputType = value;
  }

  @JsonProperty('inputValue', String)
  get inputValue(): string {
    return this._inputValue;
  }

  set inputValue(value: string) {
    this._inputValue = value;
  }

  // endregion
}
