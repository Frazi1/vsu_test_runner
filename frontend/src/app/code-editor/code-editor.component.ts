import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import 'brace'
import 'brace/mode/text'
import 'brace/mode/csharp'
import 'brace/mode/python'
import 'brace/mode/markdown'
import 'brace/theme/github'
import { CodeLanguage } from '../shared/CodeLanguage'

@Component({
  selector:    'app-code-editor',
  templateUrl: './code-editor.component.html',
  styleUrls:   ['./code-editor.component.less'],
})
export class CodeEditorComponent implements OnInit {

  constructor() {
  }


  @Input()
  public code: string

  @Input()
  public language: CodeLanguage | string

  @Output()
  private codeChange = new EventEmitter<String>()

  @Input()
  private isReadOnly = false

  public getAceLanguageId(codeLanguage: CodeLanguage | string): string {
    let languageName = (codeLanguage instanceof CodeLanguage)
      ? codeLanguage.name
      : codeLanguage
    switch (languageName) {
      case 'CSHARP':
        return 'csharp'
      case 'PYTHON':
        return 'python'
      default:
        return 'text'
    }
  }

  ngOnInit() {
  }

  public textChanged() {
    this.codeChange.emit(this.code)
  }
}
