import { Component, Input, OnInit } from '@angular/core'
import { QuestionState } from '../../../shared/question-state.enum'

@Component({
  selector:    'app-question-link',
  templateUrl: './question-link.component.html',
  styleUrls:   ['./question-link.component.scss']
})
export class QuestionLinkComponent implements OnInit {
  QuestionState = QuestionState

  @Input()
  index: number

  @Input()
  state: QuestionState

  @Input()
  name: string

  constructor() { }

  ngOnInit() {
  }

}
