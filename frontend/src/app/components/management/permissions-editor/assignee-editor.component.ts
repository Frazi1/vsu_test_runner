import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { TestInstanceAssigneeDto } from '../../../shared/TestInstanceAssigneeDto'
import { GroupCacheService } from '../../../services/cache/group-cache.service'
import { UsersCacheService } from '../../../services/cache/users-cache.service'
import { UserDto } from '../../../shared/UserDto'
import { GroupDto } from '../../../shared/GroupDto'
import { mergeAll, tap } from 'rxjs/operators'
import { combineLatest, concat, merge } from 'rxjs'
import { AssigneeModel } from './AssigneeModel'
import { IQuestion } from '../../../shared/IQuestion'

export type AssigneeType = 'all' | 'user' | 'group'

@Component({
  selector:    'app-assignee-editor',
  templateUrl: './assignee-editor.component.html',
  styleUrls:   ['./assignee-editor.component.scss']
})
export class AssigneeEditorComponent implements OnInit {

  @Input()
  assignees: TestInstanceAssigneeDto[]

  @Input()
  availableQuestions: IQuestion[]

  @Input()
  assigneeType: AssigneeType = 'all'

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
      tap(() => this.allAssigneeModels = this.createAllAssignees(this.assigneeType))
    ).subscribe()
  }

  private createAllAssignees(assigneeType: AssigneeType): AssigneeModel[] {
    const users = this.users.map(u => new AssigneeModel(TestInstanceAssigneeDto.FromUser(u),
      this.assignees.filter(i => i.user != null).find(a => a.user.id === u.id) != null
    ))
    if (assigneeType === 'user') {
      return users
    }
    const groups = this.groups.map(g => new AssigneeModel(TestInstanceAssigneeDto.FromGroup(g),
      this.assignees.filter(i => i.group != null).find(a => a.group.id === a.id) != null
    ))
    if (assigneeType === 'group') {
      return groups
    }
    return users.concat(groups)
  }

  public onSelectionChange() {
    this.assigneesChange.emit(this.allAssigneeModels
                                  .filter(m => m.isSelected)
                                  .map(m => m.assigneeDto)
    )
  }

  public hasItems(): boolean {
    return this.allAssigneeModels && this.allAssigneeModels.length > 0
  }
}
