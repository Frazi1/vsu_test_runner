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


  public isPassed(iteration: CodeExecutionResponseDto): boolean {
    return iteration.isValid === true
  }

  public isFailed(iteration: CodeExecutionResponseDto): boolean {
    return iteration.isValid === false
  }

  public isError(iteration: CodeExecutionResponseDto): boolean {
    const errors = [
      'CompileError',
      'RuntimeError',
      'TimeOutExceeded'
    ]
    return errors.some(e => iteration.status.toString() === e.toString())
  }

  ngOnInit() {
  }


}
