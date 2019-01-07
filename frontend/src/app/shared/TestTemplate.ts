import {TestQuestionTemplate} from './TestQuestionTemplate';

export class TestTemplate {
  private _id: number;
  private _name: string;
  private _timeLimit: number;
  private _questionTemplates: TestQuestionTemplate[];


  constructor(id: number = null, name: string = '', timeLimit: number = null, questionTemplates: TestQuestionTemplate[] = []) {
    this._id = id;
    this._name = name;
    this._timeLimit = timeLimit;
    this._questionTemplates = questionTemplates;
  }

  get id(): number {
    return this._id;
  }

  set id(value: number) {
    this._id = value;
  }

  get name(): string {
    return this._name;
  }

  set name(value: string) {
    this._name = value;
  }

  get timeLimit(): number {
    return this._timeLimit;
  }

  set timeLimit(value: number) {
    this._timeLimit = value;
  }

  get questionTemplates(): TestQuestionTemplate[] {
    return this._questionTemplates;
  }

  set questionTemplates(value: TestQuestionTemplate[]) {
    this._questionTemplates = value;
  }
}
