import { Component, Input, OnInit } from '@angular/core'
import { CodeExecutionResponseDto } from '../../../shared/runner/CodeExecutionResponseDto'

@Component({
  selector:    'app-answer-iterations-viewer',
  templateUrl: './answer-iterations-viewer.component.html',
  styleUrls:   ['./answer-iterations-viewer.component.scss']
})
export class AnswerIterationsViewerComponent implements OnInit {

  constructor() { }

  @Input()
  iterations: CodeExecutionResponseDto[]


  private isPassed(iteration: CodeExecutionResponseDto): boolean {
    return iteration.isValid === true
  }

  ngOnInit() {
  }


}
