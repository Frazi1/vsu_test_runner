import { CodeRunStatus } from './CodeRunStatus'

export class CodeExecutionResponseDto {
  actualInput: string
  actualOutput: string
  expectedOutput: string
  isValid: boolean | null
  status: CodeRunStatus

  constructor(actualOutput: string = '') {
    this.actualOutput = actualOutput
  }
}
