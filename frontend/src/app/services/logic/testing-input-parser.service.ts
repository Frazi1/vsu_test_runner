import { Injectable } from '@angular/core'
import { DeclarativeFunctionInput } from '../../shared/input/DeclarativeFunctionInput'
import { DeclarativeInputItem } from '../../shared/input/DeclarativeInputItem'
import { DeclarativeInputArgumentItem } from '../../shared/input/DeclarativeInputArgumentItem'
import { CodeType } from '../../shared/CodeType'

@Injectable({
  providedIn: 'root'
})
export class TestingInputParserService {
  private ITEMS_SEPARATOR = '\n'

  constructor() { }

  public parse(text: string): DeclarativeFunctionInput {
    const res = new DeclarativeFunctionInput()

    res.items = text
      .split(this.ITEMS_SEPARATOR)
      .map(item => this.parseDeclarativeItem(item))
    return res
  }

  public parseOne(test: string): DeclarativeFunctionInput {
    const res = new DeclarativeFunctionInput()
    res.items = [this.parseDeclarativeItem(test)]
    return res
  }

  private parseDeclarativeItem(item: string): DeclarativeInputItem {
    let res = new DeclarativeInputItem()
    let argumentItem = new DeclarativeInputArgumentItem()
    argumentItem.inputType = new CodeType('STRING')
    argumentItem.argumentIndex = 0
    argumentItem.inputValue = item

    res.argumentItems = [argumentItem]

    return res
  }

  public dump(input: DeclarativeFunctionInput): string {
    return input.items.map(i => this.dumpDeclarativeItem(i)).join(this.ITEMS_SEPARATOR)
  }

  private dumpDeclarativeItem(item: DeclarativeInputItem): string {
    return item.argumentItems[0].inputValue
  }
}
