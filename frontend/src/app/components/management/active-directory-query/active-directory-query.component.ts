import { Component, OnInit } from '@angular/core'
import { ActiveDirectorySearchRequestDto } from '../../../shared/ActiveDirectorySearchRequestDto'
import { LdapIntegrationService } from '../../../services/ldap-integration.service'
import { map, retry, switchMap, takeUntil, tap } from 'rxjs/operators'
import { BaseComponent } from '../../base.component'
import { Observable, Subject } from 'rxjs'
import { UserDto } from '../../../shared/UserDto'

@Component({
  selector:    'app-active-directory-query',
  templateUrl: './active-directory-query.component.html',
  styleUrls:   ['./active-directory-query.component.scss']
})
export class ActiveDirectoryQueryComponent extends BaseComponent implements OnInit {

  searchRequest: ActiveDirectorySearchRequestDto

  userProperties: string[]
  foundUsers: UserDto[]
  foundUsersObs: Observable<UserDto[]>

  search$ = new Subject()

  constructor(private ldapIntergrationService: LdapIntegrationService) {
    super()
  }

  ngOnInit() {
    this.searchRequest = new ActiveDirectorySearchRequestDto()

    this.ldapIntergrationService.getUserProperties().pipe(
      takeUntil(this.onDestroy$),
      map(res => this.filterUserProperties(res)),
      tap(res => this.userProperties = res)
    ).subscribe()

    this.foundUsersObs = this.search$.pipe(
      takeUntil(this.onDestroy$),
      switchMap(() => this.ldapIntergrationService.searcADForUsers(this.searchRequest)),
      retry(),
      tap(res => this.foundUsers = res)
    )
    this.foundUsersObs.subscribe()
  }

  private filterUserProperties(props: string[]): string[] {
    const excluded = ['Id', 'Type', 'Groups']
    return props.filter(p => !excluded.includes(p))
  }

  public canImportUsers(): boolean {
    return this.foundUsers && this.foundUsers.length && this.foundUsers.length > 0
  }
}
