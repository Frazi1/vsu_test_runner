import { Component, Input, OnInit } from '@angular/core'
import { TestRunQuestion } from '../../../shared/runner/TestRunQuestion'
import { CodeService } from '../../../services/code.service'
import { CodeSnippet } from '../../../shared/CodeSnippet'
import { CodeLanguage } from '../../../shared/CodeLanguage'
import { CodeExecutionRequest } from '../../../shared/runner/CodeExecutionRequest'

@Component({
  selector:    'app-question-runner',
  templateUrl: './question-runner.component.html',
  styleUrls:   ['./question-runner.component.less']
})
export class QuestionRunnerComponent implements OnInit {
  private _questionRun: TestRunQuestion
  private _code: string
  private _codeLanguages: CodeLanguage[]
  private _isReady = false

  constructor(private codeService: CodeService) {

    // // TODO: fix
    // this._questionRunObs.pipe(
    //   mergeMap(_ => codeService.languages()),
    //   tap(langs => this._codeLanguages = langs),
    //   mergeMap(_ => this.codeService.scaffoldFunction(this.questionRun.functionId, this._codeLanguages[0])),
    // ).subscribe((res: FunctionScaffoldingDto) => {
    //   this.questionRun.answerCodeSnippet =
    //     new CodeSnippet(null, res.codeLanguage, res.code.split('\n'), res.functionObj);
    //   this._code = this.questionRun.answerCodeSnippet.code.join('\n');
    // });
  }

  async ngOnInit() {
    this._codeLanguages = await this.codeService.languages().toPromise()
    this._isReady = true
    await this.update()
  }

  get questionRun(): TestRunQuestion {
    return this._questionRun
  }

  @Input()
  set questionRun(value: TestRunQuestion) {
    this._questionRun = value
    if (this._isReady) {
      this.update()
    }
  }

  private async update() {
    if (this.questionRun.answerCodeSnippet == null) {
      const codeLanguage = this._codeLanguages[0]
      const scaffold = await this.codeService.scaffoldFunction(this.questionRun.functionId, codeLanguage).toPromise()
      this.questionRun.answerCodeSnippet = new CodeSnippet(null,
        codeLanguage,
        scaffold.code.split('\n'),
        scaffold.functionObj
      )
    }
    this._code = this.questionRun.answerCodeSnippet.code
  }

  private async runCode() {
    const snippet = this._questionRun.answerCodeSnippet
    const req = CodeExecutionRequest.fromReturnType(snippet.language, this._code, snippet.functionObj.returnType, true)
    const res = await this.codeService.runCode(req).toPromise()
    console.log(res.codeRunResult)
  }
}
