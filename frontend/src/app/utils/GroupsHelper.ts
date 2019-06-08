import { GroupDto } from '../shared/GroupDto'
import { LookupHelper } from './LookupHelper'

export class GroupsHelper {
  public static setGroupRelations(groups: GroupDto[]): Map<string, GroupDto[]> {
    const lookup = LookupHelper.createLookup(g => (g.parentGroupId || '').toString(), groups)
    const roots: GroupDto[] = lookup[''] || []
    roots.forEach(r => this.setChildGroups(r, lookup))
    return lookup
  }

  private static setChildGroups(current: GroupDto, lookup: Map<string, GroupDto[]>) {
    const children: GroupDto[] = lookup[current.id.toString()] || []
    current.childrenGroups = children
    children.forEach(c => this.setChildGroups(c, lookup))
  }
}
