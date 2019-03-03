import { DeclarativeFunctionInput } from './DeclarativeFunctionInput'
import { Type } from 'class-transformer'

export class FunctionTestingInputDto {

  @Type(() => DeclarativeFunctionInput)
  declarativeInput: DeclarativeFunctionInput = undefined
}
