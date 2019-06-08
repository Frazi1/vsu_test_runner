import { GroupDto } from './GroupDto'

export class UserDto {
  id: number
  email: string
  userName: string

  groups: GroupDto = []
}
