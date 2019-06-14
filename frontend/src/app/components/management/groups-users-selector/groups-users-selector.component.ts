import { Component, Input, OnInit } from '@angular/core'
import { GroupDto } from '../../../shared/GroupDto'
import { UsersCacheService } from '../../../services/cache/users-cache.service'
import { BaseComponent } from '../../base.component'
import { merge, Observable, Subject } from 'rxjs'
import { UserDto } from '../../../shared/UserDto'
import { filter, flatMap, map, startWith, switchMap, takeUntil, tap } from 'rxjs/operators'
import { flatten } from '@angular/compiler'

@Component({
  selector:    'app-groups-users-selector',
  templateUrl: './groups-users-selector.component.html',
  styleUrls:   ['./groups-users-selector.component.scss']
})
export class GroupsUsersSelectorComponent extends BaseComponent implements OnInit {
  @Input()
  group: GroupDto

  users$: Observable<UserDto[]>

  groupUsers$: Observable<UserDto[]>
  availableUsers$: Observable<UserDto[]>

  selectedGroupUser: UserDto
  selectedAvailableUser: UserDto

  update$ = new Subject()

  constructor(private userCacheService: UsersCacheService) {
    super()
  }

  public ngOnInit(): void {
    this.users$ = this.userCacheService.getCached(true).pipe(
      takeUntil(this.onDestroy$)
    )

    this.groupUsers$ = this.update$.pipe(
      takeUntil(this.onDestroy$),
      startWith(true),
      // tap(() => console.log('this.groupUsers$ update')),
      switchMap(() => this.users$),
      map((users: UserDto[]) => this.group.users)
    )

    this.availableUsers$ = this.update$.pipe(
      takeUntil(this.onDestroy$),
      startWith(true),
      // tap(() => console.log('this.availableUsers$ update')),
      switchMap(() => this.users$),
      map(users => users.filter(grUser => !this.group.users.some(u => u.id === grUser.id)))
    )
  }

  public moveLeft() {
    this.group.users.push(this.selectedAvailableUser)
    this.selectedAvailableUser = null
    this.update$.next()
  }

  public moveRight() {
    this.group.users = this.group.users.filter(x => x.id != this.selectedGroupUser.id)
    this.selectedGroupUser = null
    this.update$.next()
  }

  public selectAvailableUser(u: UserDto) {
    this.selectedAvailableUser = u
  }

  public selectGroupUser(u: UserDto) {
    this.selectedGroupUser = u
  }
}

