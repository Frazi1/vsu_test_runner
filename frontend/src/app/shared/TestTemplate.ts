import {TestQuestionTemplate} from './TestQuestionTemplate';
import {JsonObject, JsonProperty} from 'json2typescript';

@JsonObject('TestTemplate')
export class TestTemplate {

  @JsonProperty('id', Number)
  public id: number;

  @JsonProperty('name', String)
  public name: string;

  @JsonProperty('timeLimit', Number, true)
  public timeLimit: number;

  @JsonProperty('questionTemplates', [TestQuestionTemplate])
  public questionTemplates: TestQuestionTemplate[];

  constructor(id: number = null, name: string = '', timeLimit: number = null, questionTemplates: TestQuestionTemplate[] = []) {
    this.id = id;
    this.name = name;
    this.timeLimit = timeLimit;
    this.questionTemplates = questionTemplates;
  }
}
