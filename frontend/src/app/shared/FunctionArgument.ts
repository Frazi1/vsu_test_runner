import { CodeType } from './CodeType';
import { JsonObject, JsonProperty } from 'json2typescript';

@JsonObject('FunctionArgument')
export class FunctionArgument {
  @JsonProperty('name', String)
  public name: string;

  @JsonProperty('type', CodeType)
  public type: CodeType;


  constructor(name: string, type: CodeType) {
    this.name = name;
    this.type = type;
  }
}
