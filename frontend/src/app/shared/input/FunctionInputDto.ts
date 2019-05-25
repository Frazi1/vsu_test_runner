import { DeclarativeFunctionInput } from './DeclarativeFunctionInput'
import { Type } from 'class-transformer'

export class TestingInputDto {

  id: number
  input: string
  expectedOutput: string


  constructor(id: number = undefined, input: string = undefined, expectedOutput: string = undefined) {
    this.id = id
    this.input = input
    this.expectedOutput = expectedOutput
  }
}
