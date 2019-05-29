export class CodeLanguage {
  id: string
  displayName: string

  constructor(name: string) {
    this.id = name
  }

  get name(): string {
    return this.id
  }
}
