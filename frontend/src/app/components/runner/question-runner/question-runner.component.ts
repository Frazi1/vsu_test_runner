import { Component, Input, OnInit } from '@angular/core'
import { QuestionAnswer } from '../../../shared/runner/QuestionAnswer'
import { CodeService } from '../../../services/code.service'
import { CodeSnippet } from '../../../shared/CodeSnippet'
import { CodeLanguage } from '../../../shared/CodeLanguage'
import { CodeExecutionRequest } from '../../../shared/runner/CodeExecutionRequest'
import { ScaffoldingType } from '../../../shared/ScaffoldingType'
import { Subject } from 'rxjs'
import { retry, retryWhen, switchMap, tap } from 'rxjs/operators'

@Component({
  selector:    'app-question-runner',
  templateUrl: './question-runner.component.html',
  styleUrls:   ['./question-runner.component.less']
})
export class QuestionRunnerComponent implements OnInit {
  private _questionRun: QuestionAnswer
  private _code: string
  private _codeLanguages: CodeLanguage[]
  private _isReady = false

  resetBtnClick$ = new Subject<void>()

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

    this.resetBtnClick$.pipe(
      tap(() => console.log('Reset btn click!')),
      switchMap(() => this.codeService
                          .getStartingSnippetForAnswer(this.questionRun.answerCodeSnippet.language, this.questionRun.id)
      ),
      tap(res => this.questionRun.answerCodeSnippet.code = res.code),
      retryWhen(errors => errors.pipe(
        tap(e => console.log(e))
      ))
    ).subscribe()
  }

  get questionRun(): QuestionAnswer {
    return this._questionRun
  }

  @Input()
  set questionRun(value: QuestionAnswer) {
    this._questionRun = value
    if (this._isReady) {
      this.update()
    }
  }

  async ngOnInit() {
    this._codeLanguages = await this.codeService.languages().toPromise()
    this._isReady = true
    await this.update()
  }

  private async update() {
    if (this.questionRun.answerCodeSnippet == null) {
      const codeLanguage = this._codeLanguages[0]
      const scaffold = await this.codeService.getStartingSnippetForAnswer(codeLanguage, this.questionRun.id).toPromise()
      this.questionRun.answerCodeSnippet = new CodeSnippet(null,
        codeLanguage,
        scaffold.code.split('\n'),
        scaffold.functionObj
      )
    }
    this._code = this.questionRun.answerCodeSnippet.code
  }
}
