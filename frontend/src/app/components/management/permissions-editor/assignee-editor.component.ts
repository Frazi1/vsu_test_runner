import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { TestInstanceAssigneeDto } from '../../../shared/TestInstanceAssigneeDto'
import { GroupCacheService } from '../../../services/cache/group-cache.service'
import { UsersCacheService } from '../../../services/cache/users-cache.service'
import { UserDto } from '../../../shared/UserDto'
import { GroupDto } from '../../../shared/GroupDto'
import { mergeAll, tap } from 'rxjs/operators'
import { combineLatest, concat, merge } from 'rxjs'
import { AssigneeModel } from './AssigneeModel'

@Component({
  selector:    'app-assignee-editor',
  templateUrl: './assignee-editor.component.html',
  styleUrls:   ['./assignee-editor.component.scss']
})
export class AssigneeEditorComponent implements OnInit {

  @Input()
  assignees: TestInstanceAssigneeDto[]

  allAssigneeModels: AssigneeModel[]

  users: UserDto[]
  groups: GroupDto[]

  @Output()
  assigneesChange = new EventEmitter<TestInstanceAssigneeDto[]>()

  constructor(private groupCache: GroupCacheService,
              private userCache: UsersCacheService) { }

  ngOnInit() {
    let getUsers$ = this.userCache.getCached(true).pipe(
      tap(u => this.users = u)
    )
    let getGroups$ = this.groupCache.getCached(true).pipe(
      tap(g => this.groups = g)
    )
    combineLatest(getGroups$, getUsers$).pipe(
      tap(() => this.allAssigneeModels = this.createAllAssignees())
    ).subscribe()
  }

  private createAllAssignees(): AssigneeModel[] {
    const users = this.users.map(u => new AssigneeModel(TestInstanceAssigneeDto.FromUser(u),
      this.assignees.filter(i => i.user != null).find(a => a.user.id === u.id) != null))
    const groups = this.groups.map(g => new AssigneeModel(TestInstanceAssigneeDto.FromGroup(g),
      this.assignees.filter(i => i.group != null).find(a => a.group.id === a.id) != null))
    return users.concat(groups)
  }

  public onSelectionChange() {
    this.assigneesChange.emit(this.allAssigneeModels
                                  .filter(m => m.isSelected)
                                  .map(m => m.assigneeDto)
    )
  }
}
