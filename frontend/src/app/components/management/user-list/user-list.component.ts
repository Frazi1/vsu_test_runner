import { Component, Input, OnInit } from '@angular/core'
import { UsersCacheService } from '../../../services/cache/users-cache.service'
import { UserDto } from '../../../shared/UserDto'
import { BaseComponent } from '../../base.component'
import { takeUntil, tap } from 'rxjs/operators'
import { Observable } from 'rxjs'

@Component({
  selector:    'app-user-list',
  templateUrl: './user-list.component.html',
  styleUrls:   ['./user-list.component.scss']
})
export class UserListComponent extends BaseComponent implements OnInit {

  @Input()
  users: UserDto[]


  constructor() {super() }

  ngOnInit() {
  }

}
