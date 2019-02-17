import {CodeType} from './CodeType';
import {FunctionArgument} from './FunctionArgument';
import {JsonObject, JsonProperty} from 'json2typescript';


@JsonObject('Function')
export class Function {

  @JsonProperty('id')
  private _id: number = undefined;

  @JsonProperty('name', String)
  public name: string;

  @JsonProperty('returnType', CodeType)
  public returnType: CodeType;

  @JsonProperty('arguments', [FunctionArgument])
  public arguments: FunctionArgument[];

  constructor(name: string = '', returnType: CodeType = null, args: FunctionArgument[] = []) {
    this.name = name;
    this.returnType = returnType;
    this.arguments = args;
  }

  // region Getters
  get id(): number {
    return this._id;
  }

  // endregion
}
