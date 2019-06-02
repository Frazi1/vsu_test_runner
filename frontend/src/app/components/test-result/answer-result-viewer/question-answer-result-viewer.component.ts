import { Component, Input, OnInit } from '@angular/core'
import { QuestionAnswer } from '../../../shared/runner/QuestionAnswer'

@Component({
  selector:    'app-question-answer-result-viewer',
  templateUrl: './question-answer-result-viewer.component.html',
  styleUrls:   ['./question-answer-result-viewer.component.scss']
})
export class QuestionAnswerResultViewerComponent implements OnInit {

  @Input()
  questionAnswer: QuestionAnswer

  constructor() { }

  ngOnInit() {
  }

}
