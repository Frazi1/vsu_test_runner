import { Component, Input, OnDestroy, OnInit } from '@angular/core'
import { TestQuestionTemplate } from '../../../shared/TestQuestionTemplate'
import { CodeSnippet } from '../../../shared/CodeSnippet'
import { CodeService } from '../../../services/code.service'
import { ScaffoldingType } from '../../../shared/ScaffoldingType'
import { merge, Observable, Subject } from 'rxjs'
import { concatMap, filter, retryWhen, takeUntil, tap } from 'rxjs/operators'
import { CodeExecutionRequest } from '../../../shared/runner/CodeExecutionRequest'
import { TestingInputParserService } from '../../../services/logic/testing-input-parser.service'
import { CodeExecutionResponseDto } from '../../../shared/runner/CodeExecutionResponseDto'
import { CodeSnippetScaffoldingDto } from '../../../shared/code/CodeSnippetScaffoldingDto'
import { NgbModal } from '@ng-bootstrap/ng-bootstrap'
import { GeneratorListModalComponent } from '../../generator/generator-list-modal/generator-list-modal.component'
import { InputGeneratorDto } from '../../../shared/code/InputGeneratorDto'
import { GeneratorRunnerModalComponent } from '../../generator/generator-runner-modal/generator-runner-modal.component'
import { ActivatedRoute } from '@angular/router'
import { BaseComponent } from '../../base.component'

@Component({
  selector:    'app-test-question-template-editor',
  templateUrl: './test-question-template-editor.component.html',
  styleUrls:   ['./test-question-template-editor.component.scss']
})
export class TestQuestionTemplateEditorComponent extends BaseComponent implements OnInit, OnDestroy {

  constructor(private codeService: CodeService,
              private testingInputParserService: TestingInputParserService,
              private modalService: NgbModal,
              private route: ActivatedRoute) {
    super()

    this.textInputChangeSub()
  }

// region Getters/Setters

  private _question: TestQuestionTemplate
  private _question$ = new Subject()

  get question(): TestQuestionTemplate {
    return this._question
  }

  private _canEdit: boolean

  @Input() set question(value: TestQuestionTemplate) {
    this._question = value
    this._question$.next(value)
  }

  get canEdit(): boolean {
    return this._canEdit
  }

  @Input()
  set canEdit(value: boolean) {
    this._canEdit = value
    this._canEdit$.next(value)
  }

  private _canEdit$ = new Subject()

  textInput: string

  codeExecutionOutput$ = new Subject<CodeExecutionResponseDto>()

  inputGenerator: InputGeneratorDto

  private _codeRunBtn$ = new Subject<void>()

  public runTestsClosure = this.runTestsFromInput.bind(this)

  ngOnInit() {
    if (this.canEdit == null) {
      this.route.data.subscribe(d => this.canEdit = d['canEdit'] === 'true')
    }

    if (this.question == null) {
      this.question = this.route.snapshot.data['question']
    }
    if (this.question.codeSnippet == null) {
      this.question.codeSnippet = CodeSnippet.EMPTY()
    }

    console.log(this.question)
    this.bindTestRunnerFunction()
    this.codeRunSub()
  }

  private bindTestRunnerFunction() {
    if (this.canEdit) {
      this.runTestsClosure = this.runTestsFromInput.bind(this)
    } else {
      this.runTestsClosure = this.runTestsByQuestionId.bind(this)
    }
  }

  private codeRunSub() {
    this._codeRunBtn$.pipe(
      takeUntil(this.onDestroy$),
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

  private textInputChangeSub(): void {
    merge(this._canEdit$, this._question$).pipe(
      takeUntil(this.onDestroy$),
      filter(() => this.question != null),
      tap(() => {
        if (this.question.testingInputs && this.canEdit) {
          this.textInput = this.testingInputParserService.dump(this.question.testingInputs)
        }
      })
    ).subscribe()
  }

  private async scaffoldSolutionFunction(): Promise<void> {
    const language = this.question.codeSnippet.language

    let snippetScaffoldingDto: CodeSnippetScaffoldingDto
    snippetScaffoldingDto = await this.codeService.scaffoldStartingSnippet(language).toPromise()
    this.question.codeSnippet.code = snippetScaffoldingDto.code
  }

  public runTestsFromInput(): Observable<CodeExecutionResponseDto[]> {
    this.onSave()
    const req = CodeExecutionRequest.fromSnippet(this.question.codeSnippet,
      ScaffoldingType.FULL_TEMPLATE,
      this.question.testingInputs
    )
    return this.codeService.runCode(req)
  }

  public runTestsByQuestionId(): Observable<CodeExecutionResponseDto[]> {
    return this.codeService.runTestsByQuestionTemplateId(this.question.id,
      CodeExecutionRequest.fromSnippet(this.question.codeSnippet, ScaffoldingType.FULL_TEMPLATE, null)
    )
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
