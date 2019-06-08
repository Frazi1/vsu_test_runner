export class GroupDto {
  id: number
  name: string
  description: string

  parentGroupId: number
  parentGroup: GroupDto
  childrenGroups: GroupDto[] = []
}
