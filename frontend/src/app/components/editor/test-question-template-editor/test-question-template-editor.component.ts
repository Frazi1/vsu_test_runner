import { Component, Input, OnDestroy, OnInit, ViewChild } from '@angular/core'
import { TestQuestionTemplate } from '../../../shared/TestQuestionTemplate'
import { Function } from '../../../shared/Function'
import { CodeSnippet } from '../../../shared/CodeSnippet'
import { CodeService } from '../../../services/code.service'
import { ScaffoldingType } from '../../../shared/ScaffoldingType'
import { Subject } from 'rxjs'
import { concatMap, concatMapTo, retry, retryWhen, switchMap, takeUntil, tap } from 'rxjs/operators'
import { CodeExecutionRequest } from '../../../shared/runner/CodeExecutionRequest'
import { CodeType } from '../../../shared/CodeType'
import { FunctionDeclarativeInputEditorComponent } from '../function-declarative-input-editor/function-declarative-input-editor.component'
import { TestingInputParserService } from '../../../services/logic/testing-input-parser.service'
import { FunctionTestingInputDto } from '../../../shared/input/FunctionInputDto'
import { CodeExecutionResponseDto } from '../../../shared/runner/CodeExecutionResponseDto'
import { FunctionScaffoldingDto } from '../../../shared/code/FunctionScaffoldingDto'

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

  textInput: string

  codeExecutionOutput$ = new Subject<CodeExecutionResponseDto>()

  private _codeRunBtn$ = new Subject<void>()
  private _unsubscribe$ = new Subject<void>()

  @ViewChild(FunctionDeclarativeInputEditorComponent)
  private declarativeInputEditorComponent: FunctionDeclarativeInputEditorComponent

  constructor(private codeService: CodeService,
              private testingInputParserService: TestingInputParserService) {
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
      tap(() => console.log('_codeRunBtn$ clicked')),
      concatMap(() => {
          return this.codeService.runCode(
            CodeExecutionRequest.fromSnippet(this.question.codeSnippet,
              ScaffoldingType.FULL_TEMPLATE,
              new FunctionTestingInputDto(this.testingInputParserService.parseOne(this.textInput))
            ))
        }
      ),
      tap(res => res.forEach(v => this.codeExecutionOutput$.next(v))),
      retryWhen(errors => errors.pipe(
        tap(e => console.log(e))
      )),
    ).subscribe()
  }

  public ngOnDestroy(): void {
    this._unsubscribe$.next()
  }


  private async scaffoldSolutionFunction(): Promise<void> {
    const language = this.question.codeSnippet.language
    const functionId = this.question.codeSnippet.functionObj.id

    let functionScaffoldingDto: FunctionScaffoldingDto
    if (functionId) {
      functionScaffoldingDto = await this.codeService.scaffoldFunction(functionId,
        language,
        ScaffoldingType.FULL_TEMPLATE
      ).toPromise()
    } else {
      functionScaffoldingDto = await this.codeService.scaffoldStartingSnippet(language).toPromise()
    }
    this.question.codeSnippet.code = functionScaffoldingDto.code
  }

  public fillFunction(question: TestQuestionTemplate, functionObj: Function): void {
    functionObj.returnType = new CodeType('STRING')
    functionObj.name = question.name != null ? question.name.toLowerCase() : ''
  }

  public onSave(): void {
    this.fillFunction(this.question, this.question.codeSnippet.functionObj)
    this.declarativeInputEditorComponent.onSave()
  }
}
