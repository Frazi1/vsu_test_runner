import {CodeType} from './CodeType';
import {FunctionArgument} from './FunctionArgument';
import {JsonObject, JsonProperty} from 'json2typescript';


@JsonObject('Function')
export class Function {
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
}
