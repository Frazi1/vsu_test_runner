import { UserDto } from './UserDto'
import { GroupDto } from './GroupDto'
import { ITestInstanceAssignee } from './ITestInstanceAssignee'
import { Type } from 'class-transformer'

export class TestInstanceAssigneeDto implements ITestInstanceAssignee {
  id: number

  @Type(() => UserDto)
  user: UserDto | undefined

  @Type(() => GroupDto)
  group: GroupDto | undefined

  public static FromUser(user: UserDto): TestInstanceAssigneeDto {
    let res = new TestInstanceAssigneeDto()
    res.user = user
    return res
  }

  public static FromGroup(group: GroupDto): TestInstanceAssigneeDto {
    let res = new TestInstanceAssigneeDto()
    res.group = group
    return res
  }

  public displayName(): string {
    if (this.user) {
      return this.user.displayName()
    }
    return this.group.displayName()
  }
}
