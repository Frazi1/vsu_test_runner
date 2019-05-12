export class CodeType {
  public static STRING = new CodeType('STRING')

  constructor(name: string = null) {
    this.name = name
  }

  name: string
}
