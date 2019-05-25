import { CodeType } from '../CodeType'
import { CodeLanguage } from '../CodeLanguage'
import { Exclude, Expose, Type } from 'class-transformer'
import { ExecutionType } from '../ExecutionType'
import { ScaffoldingType } from '../ScaffoldingType'
import { CodeSnippet } from '../CodeSnippet'
import { TestingInputDto } from '../input/FunctionInputDto'

export class CodeExecutionRequest {
  clientId: string = undefined


  @Type(() => CodeType)
  returnType: CodeType = undefined

  @Type(() => CodeLanguage)
  language: CodeLanguage = undefined

  code: string = undefined

  @Type(() => TestingInputDto)
  testingInputs: TestingInputDto[]

  @Exclude()
  private _scaffoldingType: ScaffoldingType

  private constructor(clientId: string, returnType: CodeType, language: CodeLanguage, code: string,
                      scaffoldingType: ScaffoldingType, testingInputs: TestingInputDto[]) {
    this.clientId = clientId
    this.returnType = returnType == null ? CodeType.STRING : returnType
    this.language = language
    this.code = code
    this.scaffoldingType = scaffoldingType
    this.testingInputs = testingInputs
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
    return new CodeExecutionRequest(clientId, returnType, language, code, scaffoldingType, null)
  }

  public static fromSnippet(snippet: CodeSnippet,
                            scaffoldingType: ScaffoldingType,
                            testingInputs: TestingInputDto[]) {
    return new CodeExecutionRequest(null,
      new CodeType('STRING'),
      snippet.language,
      snippet.code,
      scaffoldingType,
      testingInputs
    )
  }

}
