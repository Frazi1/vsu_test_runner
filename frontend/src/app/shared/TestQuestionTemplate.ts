import {Function} from './Function';
import {CodeType} from './CodeType';
import {JsonObject, JsonProperty} from 'json2typescript';

@JsonObject('TestQuestionTemplate')
export class TestQuestionTemplate {
  @JsonProperty('name', String)
  public name: string;

  @JsonProperty('description', String)
  public description: string;

  @JsonProperty('timeLimit', String, true)
  public timeLimit: number;

  @JsonProperty('solutionFunction', Function)
  public functionObj: Function;

  get getFunctionSignature(): Function {
    return this.functionObj;
  }

  constructor(name: string = '',
              text: string = '',
              timeLimit: number = null,
              functionSignature: Function = null) {
    this.name = name;
    this.description = text;
    this.timeLimit = timeLimit;
    this.functionObj = functionSignature;
  }
}
