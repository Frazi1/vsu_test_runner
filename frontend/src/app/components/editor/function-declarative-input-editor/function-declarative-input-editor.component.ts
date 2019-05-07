import { Component, Input, OnDestroy, OnInit } from '@angular/core'
import { DeclarativeFunctionInput } from '../../../shared/input/DeclarativeFunctionInput'
import { DeclarativeInputItem } from '../../../shared/input/DeclarativeInputItem'
import { DeclarativeInputArgumentItem } from '../../../shared/input/DeclarativeInputArgumentItem'
import { Function } from '../../../shared/Function'
import { Subject } from 'rxjs'
import { filter, retry, tap } from 'rxjs/internal/operators'
import { FunctionTestingInputDto } from '../../../shared/input/FunctionInputDto'
import { TestingInputParserService } from '../../../services/logic/testing-input-parser.service'

@Component({
  selector:    'app-function-declarative-input-editor',
  templateUrl: './function-declarative-input-editor.component.html',
  styleUrls:   ['./function-declarative-input-editor.component.less']
})
export class FunctionDeclarativeInputEditorComponent implements OnInit, OnDestroy {
  @Input()
  public functionObj: Function
  private _input: string


  constructor(private testingInputParser: TestingInputParserService) {

  }


  ngOnInit() {
    if (this.functionObj.testingInput && this.functionObj.testingInput.declarativeInput) {
      this._input = this.testingInputParser.dump(this.functionObj.testingInput.declarativeInput)
    }
  }

  public onSave(): void {
    this.functionObj.testingInput.declarativeInput = this.testingInputParser.parse(this._input)
  }

  ngOnDestroy(): void {
  }


}
