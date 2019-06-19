import { Component, Input, OnInit } from '@angular/core'
import { UsersCacheService } from '../../../services/cache/users-cache.service'
import { BaseComponent } from '../../base.component'
import { TestTemplateUserPermissionsService } from '../../../services/test-template-user-permissions.service'
import { TestTemplateUserPermissionsDto } from '../../../shared/TestTemplateUserPermissionsDto'
import { UserDto } from '../../../shared/UserDto'
import { map, switchMap, takeUntil, tap } from 'rxjs/operators'
import { combineLatest, merge, Observable, Subject } from 'rxjs'

@Component({
  selector:    'app-test-template-permissions-editor',
  templateUrl: './test-template-permissions-editor.component.html',
  styleUrls:   ['./test-template-permissions-editor.component.scss']
})
export class TestTemplatePermissionsEditorComponent extends BaseComponent implements OnInit {

  @Input()
  testTemplateId: number

  @Input()
  showSaveButton: boolean = true

  existingPermissions: TestTemplateUserPermissionsDto[]
  users: UserDto[]

  allPermissions: TestTemplateUserPermissionsDto[]

  saveClick$ = new Subject<void>()

  constructor(private userCache: UsersCacheService,
              private testTemplateUserPermissionsService: TestTemplateUserPermissionsService) {
    super()
  }

  ngOnInit() {
    let users$ = this.userCache.getCached(true).pipe(
      tap(res => this.users = res)
    )

    let permissions$ = this.testTemplateUserPermissionsService.getByTestTemplateId(this.testTemplateId).pipe(
      tap(res => this.existingPermissions = res),
    )

    const save$ = this.saveClick$.pipe(
      takeUntil(this.onDestroy$),
      switchMap(() =>
        this.testTemplateUserPermissionsService.updateByTestTemplateId(this.testTemplateId, this.allPermissions))
    ).subscribe()

    combineLatest(users$, permissions$).pipe(
      takeUntil(this.onDestroy$),
      map(pair => ({users: pair[0], permissions: pair[1]})),
      map(p => p.permissions.concat(this.createEmptyPermissions(p.users, p.permissions, this.testTemplateId))),
      tap(allPermissions => this.allPermissions = allPermissions)
    ).subscribe()
  }

  private createEmptyPermissions(users: UserDto[],
                                 existingPermissions: TestTemplateUserPermissionsDto[],
                                 testTemplateId: number): TestTemplateUserPermissionsDto[] {
    const missingUsers = users.filter(u => !existingPermissions.some(p => p.userId === u.id))
    const missingPermissions = missingUsers.map(u => {
      let p = new TestTemplateUserPermissionsDto()
      p.userId = u.id
      p.testTemplateId = testTemplateId
      p.user = u
      return p
    })
    return missingPermissions
  }
}
