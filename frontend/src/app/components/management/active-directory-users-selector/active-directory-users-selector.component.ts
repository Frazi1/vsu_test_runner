import { Component, Input, OnInit } from '@angular/core'
import { UserDto } from '../../../shared/UserDto'
import { BaseComponent } from '../../base.component'

@Component({
  selector:    'app-active-directory-users-selector',
  templateUrl: './active-directory-users-selector.component.html',
  styleUrls:   ['./active-directory-users-selector.component.scss']
})
export class ActiveDirectoryUsersSelectorComponent extends BaseComponent implements OnInit {

  @Input()
  users: UserDto[]

  constructor() {
    super()
  }

  ngOnInit() {
  }

}
