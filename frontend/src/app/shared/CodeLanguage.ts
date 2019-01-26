import {JsonObject, JsonProperty} from 'json2typescript';

@JsonObject('CodeLanguage')
export class CodeLanguage {
  @JsonProperty('name', String)
  public name: string;

  constructor(name: string) {
    this.name = name;
  }
}
