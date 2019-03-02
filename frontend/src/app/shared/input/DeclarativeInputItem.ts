import {JsonObject, JsonProperty} from 'json2typescript';
import {DeclarativeInputArgumentItem} from './DeclarativeInputArgumentItem';

@JsonObject('DeclarativeInputItem')
export class DeclarativeInputItem {
  private _id: number = undefined;
  private _argumentItems: DeclarativeInputArgumentItem[] = undefined;
  private _outputValue: string = undefined;

  @JsonProperty('id', Number)
  get id(): number {
    return this._id;
  }

  set id(value: number) {
    this._id = value;
  }

  @JsonProperty('argumentItems', [DeclarativeInputArgumentItem])
  get argumentItems(): DeclarativeInputArgumentItem[] {
    return this._argumentItems;
  }

  set argumentItems(value: DeclarativeInputArgumentItem[]) {
    this._argumentItems = value;
  }

  @JsonProperty('outputValue', String)
  get outputValue(): string {
    return this._outputValue;
  }

  set outputValue(value: string) {
    this._outputValue = value;
  }
}
