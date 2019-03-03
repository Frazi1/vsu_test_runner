import { CodeType } from '../CodeType'
import { CodeLanguage } from '../CodeLanguage'
import { Type } from 'class-transformer'

export class CodeExecutionRequest {
  clientId: string = undefined


  @Type(() => CodeType)
  returnType: CodeType = undefined

  functionId: number = undefined

  @Type(() => CodeLanguage)
  language: CodeLanguage = undefined

  code: string = undefined

  isPlainCode: boolean = undefined

  private constructor(clientId: string, returnType: CodeType, functionId: number, language: CodeLanguage, code: string,
                      isPlainCode: boolean) {
    this.clientId = clientId
    this.returnType = returnType
    this.functionId = functionId
    this.language = language
    this.code = code
    this.isPlainCode = isPlainCode
  }


  public static fromReturnType(language: CodeLanguage, code: string, returnType: CodeType, isPlainCode: boolean,
                               clientId: string = null): CodeExecutionRequest {
    return new CodeExecutionRequest(clientId, returnType, null, language, code, isPlainCode)
  }

  public static fromFunctionId(language: CodeLanguage, code: string, functionId: number, isPlainCode: boolean,
                               clientId: string = null): CodeExecutionRequest {
    return new CodeExecutionRequest(clientId, null, functionId, language, code, isPlainCode)
  }

}
