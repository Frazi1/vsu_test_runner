export class TestQuestionTemplate {
  private _name: string;
  private _text: string;
  private _timeLimit: number;


  constructor(name: string = '', text: string = '', timeLimit: number = null) {
    this._name = name;
    this._text = text;
    this._timeLimit = timeLimit;
  }

  get name(): string {
    return this._name;
  }

  set name(value: string) {
    this._name = value;
  }

  get text(): string {
    return this._text;
  }

  set text(value: string) {
    this._text = value;
  }

  get timeLimit(): number {
    return this._timeLimit;
  }

  set timeLimit(value: number) {
    this._timeLimit = value;
  }
}
