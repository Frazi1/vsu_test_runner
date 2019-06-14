import { UserDto } from './UserDto'
import { IDisplayName } from './IDisplayName'

export class GroupDto implements IDisplayName {
  id: number
  name: string
  description: string

  parentGroupId: number
  parentGroup: GroupDto
  childrenGroups: GroupDto[] = []
  users: UserDto[] = []

  public displayName(): string {
    return this.name
  }
}
