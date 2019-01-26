import {CodeType} from './CodeType';
import {FunctionArgument} from './FunctionArgument';
import {CodeSnippet} from './CodeSnippet';
import {JsonObject, JsonProperty} from 'json2typescript';


@JsonObject('Function')
export class Function {
  @JsonProperty('name', String)
  public name: string;

  @JsonProperty('returnType', CodeType)
  public returnType: CodeType;

  @JsonProperty('arguments', [FunctionArgument])
  public arguments: FunctionArgument[];

  @JsonProperty('codeSnippet', CodeSnippet)
  public codeSnippet: CodeSnippet;


  constructor(name: string, returnType: CodeType, args: FunctionArgument[] = [], codeSnippet = null) {
    this.name = name;
    this.returnType = returnType;
    this.arguments = args;
    this.codeSnippet = codeSnippet;
  }
}
