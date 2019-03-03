export class TestInstanceUpdate {

  availableAfter: Date = undefined
  disabledAfter: Date = undefined
  timeLimit: number = undefined

  constructor(availableAfter: Date, disabledAfter: Date, timeLimit: number) {
    this.availableAfter = availableAfter
    this.disabledAfter = disabledAfter
    this.timeLimit = timeLimit
  }
}
