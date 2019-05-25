import { Injectable } from '@angular/core'
import { DeclarativeFunctionInput } from '../../shared/input/DeclarativeFunctionInput'
import { DeclarativeInputItem } from '../../shared/input/DeclarativeInputItem'
import { DeclarativeInputArgumentItem } from '../../shared/input/DeclarativeInputArgumentItem'
import { CodeType } from '../../shared/CodeType'
import { TestingInputDto } from '../../shared/input/FunctionInputDto'

@Injectable({
  providedIn: 'root'
})
export class TestingInputParserService {
  private ITEMS_SEPARATOR = '\n'

  constructor() { }

  public parse(text: string): TestingInputDto[] {
    if (!text) {
      text = ''
    }
    return text
      .split(this.ITEMS_SEPARATOR)
      .map(item => this.parseOne(item))
  }

  public parseOne(text: string): TestingInputDto {
    const res = new TestingInputDto()
    res.input = text
    return res
  }

  public dump(inputs: TestingInputDto[]): string {
    return inputs.map(i => this.dumpItem(i)).join(this.ITEMS_SEPARATOR)
  }

  private dumpItem(item: TestingInputDto): string {
    return item.input
  }
}
