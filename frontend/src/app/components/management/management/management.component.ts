import { Component, OnInit } from '@angular/core'
import { BaseComponent } from '../../base.component'
import { GroupDto } from '../../../shared/GroupDto'
import { takeUntil } from 'rxjs/operators'
import { GroupCacheService } from '../../../services/cache/group-cache.service'
import { Router } from '@angular/router'
import { Observable } from 'rxjs'
import { UserDto } from '../../../shared/UserDto'
import { UsersCacheService } from '../../../services/cache/users-cache.service'

@Component({
  selector:    'app-management',
  templateUrl: './management.component.html',
  styleUrls:   ['./management.component.scss']
})
export class ManagementComponent extends BaseComponent implements OnInit {

  groups: Observable<GroupDto[]>
  selectedGroup: GroupDto

  usersSource: Observable<UserDto[]>

  constructor(private groupCache: GroupCacheService,
              private usersCache: UsersCacheService,
              private router: Router) {
    super()
  }

  ngOnInit() {
    this.groups = this.groupCache.getCached(true).pipe(
      takeUntil(this.onDestroy$),
    )

    this.usersSource = this.usersCache.getCached(true)
  }

  public addGroupClick() {
    this.router.navigate(['management', 'group', 'new'],
      {queryParams: {parentId: this.selectedGroup ? this.selectedGroup.id : null}}
    )
  }

  selectedGroupChange(group: GroupDto) {
    this.selectedGroup = group
  }
}
