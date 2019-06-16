import { Component, OnInit } from '@angular/core'
import { UsersCacheService } from '../../../services/cache/users-cache.service'
import { UserDto } from '../../../shared/UserDto'
import { BaseComponent } from '../../base.component'
import { takeUntil, tap } from 'rxjs/operators'

@Component({
  selector:    'app-user-list',
  templateUrl: './user-list.component.html',
  styleUrls:   ['./user-list.component.scss']
})
export class UserListComponent extends BaseComponent implements OnInit {
  users: UserDto[]

  constructor(private userCache: UsersCacheService) {super() }

  ngOnInit() {
    this.userCache.getCached(true).pipe(
      takeUntil(this.onDestroy$),
      tap(res => this.users = res)
    ).subscribe()
  }

}
