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
  styleUrls:   ['./code-editor.component.scss'],
})
export class CodeEditorComponent implements OnInit {

  constructor() {
  }


  @Input()
  code: string

  @Input()
  language: CodeLanguage | string

  @Input()
  isReadOnly = false

  @Input()
  minLines = 20

  @Output()
  private codeChange = new EventEmitter<String>()


  config: AceConfigInterface

  public getAceLanguageId(codeLanguage: CodeLanguage | string): string {
    let languageName = (codeLanguage instanceof CodeLanguage)
      ? (codeLanguage.id || '').toUpperCase()
      : codeLanguage || ''

    if (languageName.includes('PYTHON')) {
      return 'python'
    }

    switch (languageName) {
      case 'CSHARP':
        return 'csharp'
      default:
        return 'text'
    }
  }

  ngOnInit() {
    this.config = {
      autoScrollEditorIntoView: true,
      minLines:                 this.minLines,
      maxLines:                 50
    }

  }

  public textChanged() {
    this.codeChange.emit(this.code)
  }
}
