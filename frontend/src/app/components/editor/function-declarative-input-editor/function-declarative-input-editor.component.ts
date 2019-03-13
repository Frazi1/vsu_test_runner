import { Component, Input, OnDestroy, OnInit } from '@angular/core'
import { DeclarativeFunctionInput } from '../../../shared/input/DeclarativeFunctionInput'
import { DeclarativeInputItem } from '../../../shared/input/DeclarativeInputItem'
import { DeclarativeInputArgumentItem } from '../../../shared/input/DeclarativeInputArgumentItem'
import { Function } from '../../../shared/Function'
import { Subject } from 'rxjs'
import { filter, retry, tap } from 'rxjs/internal/operators'
import { FunctionTestingInputDto } from '../../../shared/input/FunctionInputDto'

@Component({
  selector:    'app-function-declarative-input-editor',
  templateUrl: './function-declarative-input-editor.component.html',
  styleUrls:   ['./function-declarative-input-editor.component.less']
})
export class FunctionDeclarativeInputEditorComponent implements OnInit, OnDestroy {
  @Input()
  public functionObj: Function

  // @Input()
  // public declarativeResult: DeclarativeFunctionInput
  //
  // @Output()
  // public declarativeResultChange = new EventEmitter<DeclarativeFunctionInput>()

  private _input: string
  private _parse$ = new Subject<void>()

  private ARGUMENT_SEPARATOR_SYMBOL = ';'

  ngOnInit() {
    if (this.functionObj.testingInput) {
      this._input = this.dump(this.functionObj.testingInput.declarativeInput)
    }
    this._parse$.pipe(
      retry(),
      filter(_ => this._input != null),
      tap(_ => {
        if (!this.functionObj.testingInput) {
          this.functionObj.testingInput = new FunctionTestingInputDto()
        }

        this.functionObj.testingInput.declarativeInput = this.parse(this._input)
      }),
      tap(_ => console.log(this.functionObj.testingInput.declarativeInput)),
    ).subscribe()
  }


  ngOnDestroy(): void {
    this._parse$.unsubscribe()
  }

  private parse(text: string): DeclarativeFunctionInput {
    const res = new DeclarativeFunctionInput()
    res.items = text
      .split('\n')
      .map(i => this.parseDeclarativeItem(i))
    return res
  }

  private parseDeclarativeItem(line: string): DeclarativeInputItem {
    let res = new DeclarativeInputItem()
    const split = line.split('->')
    res.outputValue = split.length > 1 ? split[1].trim() : null
    res.argumentItems = this.parseArguments(split[0])
    return res
  }

  private parseArguments(argsLine: string): DeclarativeInputArgumentItem[] {
    return argsLine.split(this.ARGUMENT_SEPARATOR_SYMBOL)
                   .map(s => s.trim())
                   .map((s, index) => {
                     let arg = new DeclarativeInputArgumentItem()
                     arg.argumentIndex = index + 1
                     arg.inputType = this.functionObj.arguments[index].type
                     arg.inputValue = s
                     return arg
                   })
  }

  private dump(input: DeclarativeFunctionInput): string {
    return input.items.map(i => this.dumpDeclarativeItem(i)).join('\n')
  }

  private dumpDeclarativeItem(item: DeclarativeInputItem): string {
    let res = item.argumentItems.map(a => a.inputValue).join(this.ARGUMENT_SEPARATOR_SYMBOL + ' ')
    if (item.outputValue) {
      res += ` -> ${item.outputValue}`
    }
    return res
  }
}
