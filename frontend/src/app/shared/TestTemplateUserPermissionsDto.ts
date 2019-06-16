import { UserDto } from './UserDto'
import { Type } from 'class-transformer'
import { PermissionDto } from './PermissionDto'

export class TestTemplateUserPermissionsDto extends PermissionDto {
  userId: number
  testTemplateId: number

  @Type(() => UserDto)
  user: UserDto
}
