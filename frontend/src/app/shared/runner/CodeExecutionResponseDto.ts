export class CodeExecutionResponseDto {
  actualOutput: string
  expectedOutput: string
  isValid: boolean | null


  constructor(actualOutput: string = '') {
    this.actualOutput = actualOutput
  }
}
