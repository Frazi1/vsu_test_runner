import { Component, Input, OnDestroy, OnInit } from '@angular/core'
import { TestQuestionTemplate } from '../../../shared/TestQuestionTemplate'
import { Function } from '../../../shared/Function'
import { CodeSnippet } from '../../../shared/CodeSnippet'
import { CodeService } from '../../../services/code.service'
import { ScaffoldingType } from '../../../shared/ScaffoldingType'
import { Subject } from 'rxjs'
import { concatMap, concatMapTo, retry, switchMap, takeUntil, tap } from 'rxjs/operators'
import { CodeExecutionRequest } from '../../../shared/runner/CodeExecutionRequest'

@Component({
  selector:    'app-test-question-template-editor',
  templateUrl: './test-question-template-editor.component.html',
  styleUrls:   ['./test-question-template-editor.component.less']
})
export class TestQuestionTemplateEditorComponent implements OnInit, OnDestroy {

  private _editingName = false
  private _displayContent = true

  @Input()
  question: TestQuestionTemplate

  codeExecutionOutput$ = new Subject<string>()

  private _codeRunBtn$ = new Subject<void>()
  private _unsubscribe$ = new Subject<void>()


  constructor(private codeService: CodeService) {
  }

  // region Getters/Setters
  get editingName(): boolean {
    return this._editingName
  }

  set editingName(value: boolean) {
    this._editingName = value
  }

  ngOnInit() {
    if (this.question.codeSnippet == null) {
      this.question.codeSnippet = new CodeSnippet(null, null, [], new Function())
    }

    if (this.question.codeSnippet.functionObj == null) {
      this.question.codeSnippet.functionObj = new Function()
    }

    console.log(this.question)

    this._codeRunBtn$.pipe(
      takeUntil(this._unsubscribe$),
      switchMap(() => this.codeService.runCode(
        CodeExecutionRequest.fromSnippet(this.question.codeSnippet, ScaffoldingType.FULL_TEMPLATE))
      ),
      tap(res =>  res.forEach(v => this.codeExecutionOutput$.next(v.actualOutput))),
      retry()
    ).subscribe()
  }

  public ngOnDestroy(): void {

  }


  private async scaffoldSolutionFunction(): Promise<void> {
    const functionId = this.question.codeSnippet.functionObj.id
    const language = this.question.codeSnippet.language
    const functionScaffoldingDto = await this.codeService.scaffoldFunction(functionId,
      language,
      ScaffoldingType.FULL_TEMPLATE
    ).toPromise()
    this.question.codeSnippet.code = functionScaffoldingDto.code
  }
}
