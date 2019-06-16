import { GroupDto } from './GroupDto'
import { IDisplayName } from './IDisplayName'

export class UserDto implements IDisplayName {
  id: number
  email: string
  userName: string
  type: string
  groups: GroupDto[] = []
  features: number[] = []

  public displayName(): string {
    return this.userName || this.email
  }

}
