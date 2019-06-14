import { Injectable } from '@angular/core'
import { Observable } from 'rxjs'
import { GroupDto } from '../../shared/GroupDto'
import { map } from 'rxjs/operators'
import { GroupService } from '../group.service'
import { GroupsHelper } from '../../utils/GroupsHelper'
import { BaseCacheService } from './base-cache.service'

@Injectable({
  providedIn: 'root'
})
export class GroupCacheService extends BaseCacheService<GroupDto[]> {

  constructor(private groupService: GroupService) {super() }

  protected dataProvider(): () => Observable<GroupDto[]> {
    return () => this.groupService.getAll()
                     .pipe(
                       map(groups => {
                         GroupsHelper.setGroupRelations(groups)
                         return groups
                       })
                     )

  }
}
