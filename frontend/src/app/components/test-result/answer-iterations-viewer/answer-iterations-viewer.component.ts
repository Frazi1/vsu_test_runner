import { Component, Input, OnInit } from '@angular/core'
import { CodeRunIterationDto } from '../../../shared/runner/CodeRunIterationDto'

@Component({
  selector:    'app-answer-iterations-viewer',
  templateUrl: './answer-iterations-viewer.component.html',
  styleUrls:   ['./answer-iterations-viewer.component.less']
})
export class AnswerIterationsViewerComponent implements OnInit {

  constructor() { }

  @Input()
  iterations: CodeRunIterationDto[]


  private isPassed(iteration: CodeRunIterationDto): boolean {
    return iteration.actualOutput === iteration.expectedOutput
  }

  ngOnInit() {
  }


}
