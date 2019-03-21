import { CodeType } from '../CodeType'
import { CodeLanguage } from '../CodeLanguage'
import { Exclude, Expose, Type } from 'class-transformer'
import { ExecutionType } from '../ExecutionType'

export class CodeExecutionRequest {
  clientId: string = undefined


  @Type(() => CodeType)
  returnType: CodeType = undefined

  functionId: number = undefined

  @Type(() => CodeLanguage)
  language: CodeLanguage = undefined

  code: string = undefined

  @Exclude()
  private _executionType: ExecutionType = undefined

  private constructor(clientId: string, returnType: CodeType, functionId: number, language: CodeLanguage, code: string,
                      executionType: ExecutionType) {
    this.clientId = clientId
    this.returnType = returnType
    this.functionId = functionId
    this.language = language
    this.code = code
    this.executionType = executionType
  }

  @Expose()
  public get executionType(): string {
    return ExecutionType[this._executionType]
  }

  public set executionType(value) {
    this._executionType = ExecutionType[value]
  }

  public static fromReturnType(language: CodeLanguage, code: string, returnType: CodeType, executionType: ExecutionType,
                               clientId: string = null): CodeExecutionRequest {
    return new CodeExecutionRequest(clientId, returnType, null, language, code, executionType)
  }

  public static fromFunctionId(language: CodeLanguage, code: string, functionId: number, executionType: ExecutionType,
                               clientId: string = null): CodeExecutionRequest {
    return new CodeExecutionRequest(clientId, null, functionId, language, code, executionType)
  }

}
