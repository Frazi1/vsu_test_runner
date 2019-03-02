import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
  selector:    'app-code-editor',
  templateUrl: './code-editor.component.html',
  styleUrls:   ['./code-editor.component.less'],
})
export class CodeEditorComponent implements OnInit {


  @Input()
  public code: string;

  @Output()
  private codeChange = new EventEmitter<String>();

  constructor() {
  }

  ngOnInit() {
  }

  private onCodeChange(): void {
    this.codeChange.emit(this.code);
  }
}
