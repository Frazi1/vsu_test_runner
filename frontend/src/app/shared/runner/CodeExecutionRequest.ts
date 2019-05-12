import { CodeType } from '../CodeType'
import { CodeLanguage } from '../CodeLanguage'
import { Exclude, Expose, Type } from 'class-transformer'
import { ExecutionType } from '../ExecutionType'
import { ScaffoldingType } from '../ScaffoldingType'
import { CodeSnippet } from '../CodeSnippet'
import { FunctionTestingInputDto } from '../input/FunctionInputDto'

export class CodeExecutionRequest {
  clientId: string = undefined


  @Type(() => CodeType)
  returnType: CodeType = undefined

  functionId: number = undefined

  @Type(() => CodeLanguage)
  language: CodeLanguage = undefined

  code: string = undefined

  @Type(() => FunctionTestingInputDto)
  testingInput: FunctionTestingInputDto

  @Exclude()
  private _scaffoldingType: ScaffoldingType

  private constructor(clientId: string, returnType: CodeType, functionId: number, language: CodeLanguage, code: string,
                      scaffoldingType: ScaffoldingType, testingInput: FunctionTestingInputDto) {
    this.clientId = clientId
    this.returnType = returnType == null ? CodeType.STRING : returnType
    this.functionId = functionId
    this.language = language
    this.code = code
    this.scaffoldingType = scaffoldingType
    this.testingInput = testingInput
  }

  @Expose()
  public get scaffoldingType(): string {
    return ScaffoldingType[this._scaffoldingType]
  }

  public set scaffoldingType(value) {
    this._scaffoldingType = ScaffoldingType[value]
  }

  public static fromReturnType(language: CodeLanguage,
                               code: string,
                               returnType: CodeType,
                               scaffoldingType: ScaffoldingType,
                               clientId: string = null): CodeExecutionRequest {
    return new CodeExecutionRequest(clientId, returnType, null, language, code, scaffoldingType, null)
  }

  public static fromFunctionId(language: CodeLanguage,
                               code: string,
                               functionId: number,
                               scaffoldingType: ScaffoldingType,
                               clientId: string = null): CodeExecutionRequest {
    return new CodeExecutionRequest(clientId, null, functionId, language, code, scaffoldingType, null)
  }

  public static fromSnippet(snippet: CodeSnippet,
                            scaffoldingType: ScaffoldingType,
                            testingInput: FunctionTestingInputDto) {
    return new CodeExecutionRequest(null,
      snippet.functionObj.returnType,
      snippet.functionObj.id,
      snippet.language,
      snippet.code,
      scaffoldingType,
      testingInput
    )
  }

}
