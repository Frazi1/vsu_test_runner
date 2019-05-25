import { CodeType } from './CodeType'
import { FunctionArgument } from './FunctionArgument'
import { TestingInputDto } from './input/FunctionInputDto'
import { Type } from 'class-transformer'


export class Function {

  id: number = undefined
  name: string

  @Type(() => CodeType)
  returnType: CodeType


  @Type(() => FunctionArgument)
  arguments: FunctionArgument[]


  @Type(() => TestingInputDto)
  testingInput: TestingInputDto = new TestingInputDto()

  constructor(name: string = '', returnType: CodeType = null, args: FunctionArgument[] = []) {
    this.id = null
    this.name = name
    this.returnType = returnType
    this.arguments = args
  }
}
