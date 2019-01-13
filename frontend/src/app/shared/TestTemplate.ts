import {TestQuestionTemplate} from './TestQuestionTemplate';

export class TestTemplate {
  public id: number;
  public name: string;
  public timeLimit: number;
  public questionTemplates: TestQuestionTemplate[];

  constructor(id: number = null, name: string = '', timeLimit: number = null, questionTemplates: TestQuestionTemplate[] = []) {
    this.id = id;
    this.name = name;
    this.timeLimit = timeLimit;
    this.questionTemplates = questionTemplates;
  }
}
