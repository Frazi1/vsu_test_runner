import { Component, Input, OnInit } from '@angular/core'
import { TestQuestionTemplate } from '../../../shared/TestQuestionTemplate'
import { Function } from '../../../shared/Function'
import { CodeSnippet } from '../../../shared/CodeSnippet'
import { CodeService } from '../../../services/code.service'
import { ScaffoldingType } from '../../../shared/ScaffoldingType'

@Component({
  selector:    'app-test-question-template-editor',
  templateUrl: './test-question-template-editor.component.html',
  styleUrls:   ['./test-question-template-editor.component.less']
})
export class TestQuestionTemplateEditorComponent implements OnInit {

  private _editingName = false
  private _displayContent = true
  @Input()
  private question: TestQuestionTemplate

  constructor(private codeService: CodeService) {
  }

  // endregion

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
  }

  private async scaffoldSolutionFunction(): Promise<void> {
    const functionId = this.question.codeSnippet.functionObj.id
    const language = this.question.codeSnippet.language
    const functionScaffoldingDto = await this.codeService.scaffoldFunction(functionId,
      language,
      ScaffoldingType.FUNCTION_ONLY
    ).toPromise()
    this.question.codeSnippet.code = functionScaffoldingDto.code
  }

}
