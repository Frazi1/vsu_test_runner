import { CodeExecutionResult } from './CodeRunResult'
import { Type } from 'class-transformer'

export class CodeExecutionResponse {
  clientId: string = undefined
  @Type(() => CodeExecutionResult)
  codeRunResult: CodeExecutionResult = undefined
}
