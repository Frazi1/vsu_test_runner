import { Component, Input, OnInit } from '@angular/core'
import { QuestionState } from '../../../shared/question-state.enum'

@Component({
  selector:    'app-question-link',
  templateUrl: './question-link.component.html',
  styleUrls:   ['./question-link.component.less']
})
export class QuestionLinkComponent implements OnInit {
  QuestionState = QuestionState

  @Input()
  private index: number

  @Input()
  private state: QuestionState

  @Input()
  private name: string

  constructor() { }

  ngOnInit() {
  }

}
