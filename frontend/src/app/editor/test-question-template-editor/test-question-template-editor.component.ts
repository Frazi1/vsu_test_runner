import {Component, Input, OnInit} from '@angular/core';
import {TestQuestionTemplate} from '../../shared/TestQuestionTemplate';

@Component({
  selector: 'app-test-question-template-editor',
  templateUrl: './test-question-template-editor.component.html',
  styleUrls: ['./test-question-template-editor.component.less']
})
export class TestQuestionTemplateEditorComponent implements OnInit {

  private _editingName = false;

  // region Getters/Setters
  get editingName(): boolean {
    return this._editingName;
  }

  set editingName(value: boolean) {
    this._editingName = value;
  }

  // endregion

  @Input()
  private question: TestQuestionTemplate;


  constructor() {
  }

  ngOnInit() {
  }

}
