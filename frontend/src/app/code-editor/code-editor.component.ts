import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import 'brace'
import 'brace/mode/text'
import 'brace/mode/csharp'
import 'brace/mode/python'
import 'brace/mode/markdown'
import 'brace/theme/github'
import { CodeLanguage } from '../shared/CodeLanguage'
import { AceConfigInterface } from 'ngx-ace-wrapper'

@Component({
  selector:    'app-code-editor',
  templateUrl: './code-editor.component.html',
  styleUrls:   ['./code-editor.component.less'],
})
export class CodeEditorComponent implements OnInit {

  constructor() {
  }


  @Input()
  code: string

  @Input()
  language: CodeLanguage | string

  @Output()
  private codeChange = new EventEmitter<String>()

  @Input()
  isReadOnly = false

  public config: AceConfigInterface = {
    autoScrollEditorIntoView: true,
    minLines:                 10,
    maxLines:                 50
  }

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
