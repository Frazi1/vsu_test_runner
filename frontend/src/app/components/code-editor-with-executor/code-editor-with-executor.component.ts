import { Component, Input, OnDestroy, OnInit } from '@angular/core'
import { Observable, Subject } from 'rxjs'
import { CodeExecutionResponseDto } from '../../shared/runner/CodeExecutionResponseDto'
import { concatMap, retryWhen, switchMap, takeUntil, tap } from 'rxjs/operators'
import { CodeExecutionRequest } from '../../shared/runner/CodeExecutionRequest'
import { ScaffoldingType } from '../../shared/ScaffoldingType'
import { FunctionTestingInputDto } from '../../shared/input/FunctionInputDto'
import { CodeService } from '../../services/code.service'
import { TestingInputParserService } from '../../services/logic/testing-input-parser.service'
import { CodeSnippet } from '../../shared/CodeSnippet'

@Component({
  selector:    'app-code-editor-with-executor',
  templateUrl: './code-editor-with-executor.component.html',
  styleUrls:   ['./code-editor-with-executor.component.less']
})
export class CodeEditorWithExecutorComponent implements OnInit, OnDestroy {

  constructor(private codeService: CodeService,
              private testingInputParserService: TestingInputParserService) {

  }

  @Input()
  codeSnippet: CodeSnippet

  @Input()
  onRunTestsClick: () => Observable<CodeExecutionResponseDto[]>

  textInput: string
  codeExecutionOutput$ = new Subject<CodeExecutionResponseDto>()

  private _codeRunBtn$ = new Subject<void>()
  private _codeRunTestsBtn$ = new Subject<void>()
  private _unsubscribe$ = new Subject<void>()


  ngOnInit() {

    this._codeRunBtn$.pipe(
      takeUntil(this._unsubscribe$),
      tap(() => console.log('_codeRunBtn$ clicked')),
      concatMap(() =>
        this.codeService.runCode(
          CodeExecutionRequest.fromSnippet(this.codeSnippet,
            ScaffoldingType.FULL_TEMPLATE,
            new FunctionTestingInputDto(this.testingInputParserService.parseOne(this.textInput))
          ))
      ),
      tap(res => res.forEach(v => this.codeExecutionOutput$.next(v))),
      retryWhen(errors => errors.pipe(
        tap(e => console.error(e))
      )),
    ).subscribe()

    this._codeRunTestsBtn$.pipe(
      takeUntil(this._unsubscribe$),
      switchMap(() => this.onRunTestsClick()),
      tap(res => res.forEach(v => this.codeExecutionOutput$.next(v))),
      retryWhen(errors => errors.pipe(
        tap(e => console.error(e))
      )),
    ).subscribe()

  }

  public ngOnDestroy(): void {
    this._unsubscribe$.next()
  }

}
