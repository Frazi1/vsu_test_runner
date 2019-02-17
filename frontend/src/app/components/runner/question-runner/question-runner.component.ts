import {Component, Input, OnInit} from '@angular/core';
import {TestRunQuestion} from '../../../shared/runner/TestRunQuestion';

@Component({
  selector: 'app-question-runner',
  templateUrl: './question-runner.component.html',
  styleUrls: ['./question-runner.component.less']
})
export class QuestionRunnerComponent implements OnInit {
  private _questionRun: TestRunQuestion;

  constructor() {
  }

  ngOnInit() {
  }

  get questionRun(): TestRunQuestion {
    return this._questionRun;
  }

  @Input()
  set questionRun(value: TestRunQuestion) {
    this._questionRun = value;
  }
}
