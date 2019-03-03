import { CodeType } from './CodeType'
import { FunctionArgument } from './FunctionArgument'
import { FunctionTestingInputDto } from './input/FunctionInputDto'
import { Type } from 'class-transformer'


export class Function {

  id: number = undefined
  name: string

  @Type(() => CodeType)
  returnType: CodeType


  @Type(() => FunctionArgument)
  arguments: FunctionArgument[]


  @Type(() => FunctionTestingInputDto)
  testingInput: FunctionTestingInputDto = new FunctionTestingInputDto()

  constructor(name: string = '', returnType: CodeType = null, args: FunctionArgument[] = []) {
    this.id = null
    this.name = name
    this.returnType = returnType
    this.arguments = args
  }
}
