import { Component, OnInit } from '@angular/core'
import { BaseComponent } from '../../base.component'
import { GroupDto } from '../../../shared/GroupDto'
import { takeUntil, tap } from 'rxjs/operators'
import { GroupCacheService } from '../../../services/cache/group-cache.service'
import { Router } from '@angular/router'

@Component({
  selector:    'app-management',
  templateUrl: './management.component.html',
  styleUrls:   ['./management.component.scss']
})
export class ManagementComponent extends BaseComponent implements OnInit {

  groups: GroupDto[]

  constructor(private groupCache: GroupCacheService,
              private router: Router) {
    super()
  }

  ngOnInit() {
    this.groupCache.groups.pipe(
      takeUntil(this.onDestroy$),
      tap(groups => this.groups = groups)
    ).subscribe()
  }

  public addGroupClick(parentId: number | undefined | null) {
    let path = ['management', 'group', 'new']
    if (typeof parentId === 'number') {
      path.push(parentId.toString())
    }
    this.router.navigate(path)
  }
}
