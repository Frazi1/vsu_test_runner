import {Component, OnInit} from '@angular/core';
import {TestQuestionTemplate} from '../../shared/TestQuestionTemplate';

@Component({
  selector: 'app-test-question-template-editor',
  templateUrl: './test-question-template-editor.component.html',
  styleUrls: ['./test-question-template-editor.component.less']
})
export class TestQuestionTemplateEditorComponent implements OnInit {

  public testQuestionTemplate: TestQuestionTemplate;

  constructor() {
  }

  ngOnInit() {
  }

}
