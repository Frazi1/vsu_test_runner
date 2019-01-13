export class TestQuestionTemplate {
  private name: string;
  private text: string;
  private timeLimit: number;


  constructor(name: string = '', text: string = '', timeLimit: number = null) {
    this.name = name;
    this.text = text;
    this.timeLimit = timeLimit;
  }
}
