export class TestQuestionTemplate {
  public name: string;
  public description: string;
  public timeLimit: number;


  constructor(name: string = '', text: string = '', timeLimit: number = null) {
    this.name = name;
    this.description = text;
    this.timeLimit = timeLimit;
  }
}
