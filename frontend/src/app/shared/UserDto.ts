import { GroupDto } from './GroupDto'
import { IDisplayName } from './IDisplayName'

export class UserDto implements IDisplayName {
  id: number
  email: string
  userName: string
  firstName: string
  middleName: string
  lastName: string
  type: string
  groups: GroupDto[] = []
  features: number[] = []

  public displayName(): string {
    if (this.firstName && this.lastName) {
      const res = []
      res.push(this.firstName)
      if (this.middleName) {
        res.push(` ${this.middleName}`)
      }
      res.push(` ${this.lastName}`)
      return res.reduce((val, i) => val + i)
    }
    return this.userName || this.email
  }

}
