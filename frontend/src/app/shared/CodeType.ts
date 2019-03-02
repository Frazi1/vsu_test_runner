import { JsonObject, JsonProperty } from 'json2typescript'

@JsonObject('CodeType')
export class CodeType {

  @JsonProperty('name', String)
  public name: string

  constructor(name: string = null) {
    this.name = name
  }
}
