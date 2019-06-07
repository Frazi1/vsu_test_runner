import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { BaseComponent } from '../../base.component'
import { ActivatedRoute } from '@angular/router'
import { retry, retryWhen, switchMap, takeUntil, takeWhile, tap } from 'rxjs/operators'
import { InputGeneratorDto } from '../../../shared/code/InputGeneratorDto'
import { Subject } from 'rxjs'
import { CodeService } from '../../../services/code.service'
import { CodeExecutionResponseDto } from '../../../shared/runner/CodeExecutionResponseDto'

@Component({
  selector:    'app-generator-runner',
  templateUrl: './generator-runner.component.html',
  styleUrls:   ['./generator-runner.component.scss']
})
export class GeneratorRunnerComponent extends BaseComponent implements OnInit {

  @Input()
  generator: InputGeneratorDto

  apply$ = new Subject()

  result: string

  @Output()
  resultChange = new EventEmitter<string>()

  constructor(private codeService: CodeService) {
    super()
  }

  public ngOnInit(): void {
    // this.activatedRoute.data.pipe(
    //   tap(data => this.generator = data as InputGeneratorDto)
    // ).subscribe()

    this.apply$.pipe(
      takeUntil(this.onDestroy$),
      retry(),
      switchMap(() => this.codeService.applyGenerator(this.generator)),
      tap(resp => this.setResult(resp))
    ).subscribe()
  }

  private setResult(value: CodeExecutionResponseDto) {
    let res = value.actualOutput
    this.result = res
    this.resultChange.emit(res)
  }

}
