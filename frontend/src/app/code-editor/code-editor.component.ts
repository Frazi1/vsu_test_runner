import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import 'brace'
import 'brace/mode/text'
import 'brace/mode/csharp'
import 'brace/mode/python'
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
  public language: CodeLanguage

  @Output()
  private codeChange = new EventEmitter<String>()

  @Input()
  private isReadOnly = false

  public getAceLanguageId(codeLanguage: CodeLanguage): string {
    switch (codeLanguage.name) {
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

  private onCodeChange(): void {
    this.codeChange.emit(this.code)
  }
}
