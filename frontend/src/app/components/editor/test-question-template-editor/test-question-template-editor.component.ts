import { Component, Input, OnDestroy, OnInit, ViewChild } from '@angular/core'
import { TestQuestionTemplate } from '../../../shared/TestQuestionTemplate'
import { CodeSnippet } from '../../../shared/CodeSnippet'
import { CodeService } from '../../../services/code.service'
import { ScaffoldingType } from '../../../shared/ScaffoldingType'
import { Observable, Subject } from 'rxjs'
import { concatMap, retryWhen, takeUntil, tap } from 'rxjs/operators'
import { CodeExecutionRequest } from '../../../shared/runner/CodeExecutionRequest'
import { TestingInputParserService } from '../../../services/logic/testing-input-parser.service'
import { CodeExecutionResponseDto } from '../../../shared/runner/CodeExecutionResponseDto'
import { CodeSnippetScaffoldingDto } from '../../../shared/code/CodeSnippetScaffoldingDto'
import { NgbModal } from '@ng-bootstrap/ng-bootstrap'
import { GeneratorListComponent } from '../../generator/generator-list/generator-list.component'
import { GeneratorListModalComponent } from '../../generator/generator-list-modal/generator-list-modal.component'
import { InputGeneratorDto } from '../../../shared/code/InputGeneratorDto'
import { GeneratorRunnerModalComponent } from '../../generator/generator-runner-modal/generator-runner-modal.component'

@Component({
  selector:    'app-test-question-template-editor',
  templateUrl: './test-question-template-editor.component.html',
  styleUrls:   ['./test-question-template-editor.component.scss']
})
export class TestQuestionTemplateEditorComponent implements OnInit, OnDestroy {

  constructor(private codeService: CodeService,
              private testingInputParserService: TestingInputParserService,
              private modalService: NgbModal) {
  }

  // region Getters/Setters
  get editingName(): boolean {
    return this._editingName
  }

  set editingName(value: boolean) {
    this._editingName = value
  }

  private _editingName = false
  displayContent = true

  @Input()
  question: TestQuestionTemplate

  textInput: string

  codeExecutionOutput$ = new Subject<CodeExecutionResponseDto>()

  inputGenerator: InputGeneratorDto

  private _codeRunBtn$ = new Subject<void>()
  private _unsubscribe$ = new Subject<void>()

  public runTestsClosure = this.runTests.bind(this)

  ngOnInit() {
    if (this.question.codeSnippet == null) {
      this.question.codeSnippet = CodeSnippet.EMPTY()
    }

    if (this.question.testingInputs) {
      this.textInput = this.testingInputParserService.dump(this.question.testingInputs)
    }

    console.log(this.question)

    this._codeRunBtn$.pipe(
      takeUntil(this._unsubscribe$),
      tap(() => console.log('_codeRunBtn$ clicked')),
      concatMap(() => {
          return this.codeService.runCode(
            CodeExecutionRequest.fromSnippet(this.question.codeSnippet,
              ScaffoldingType.FULL_TEMPLATE,
              this.testingInputParserService.parse(this.textInput)
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

    let snippetScaffoldingDto: CodeSnippetScaffoldingDto
    snippetScaffoldingDto = await this.codeService.scaffoldStartingSnippet(language).toPromise()
    this.question.codeSnippet.code = snippetScaffoldingDto.code
  }

  public runTests(): Observable<CodeExecutionResponseDto[]> {
    this.onSave()
    const req = CodeExecutionRequest.fromSnippet(this.question.codeSnippet,
      ScaffoldingType.FULL_TEMPLATE,
      this.question.testingInputs
    )
    return this.codeService.runCode(req)
  }

  public onSave(): void {
    this.question.testingInputs = this.testingInputParserService.parse(this.textInput)
  }

  public openGeneratorSelectionModal(): void {
    const modalRef = this.modalService.open(GeneratorListModalComponent)
    modalRef.result
            .then(generator => this.inputGenerator = generator)
  }

  public openGeneratorRunnerModal(): void {
    const modalRef = this.modalService.open(GeneratorRunnerModalComponent)
    modalRef.componentInstance.generator = this.inputGenerator
    modalRef.result.then(res => this.textInput = res)
  }
}
