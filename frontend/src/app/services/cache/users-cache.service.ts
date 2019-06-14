import { BaseCacheService } from './base-cache.service'
import { UserDto } from '../../shared/UserDto'
import { Observable } from 'rxjs'
import { UserService } from '../user.service'
import { Injectable } from '@angular/core'

@Injectable({
  providedIn: 'root'
})
export class UsersCacheService extends BaseCacheService<UserDto[]> {

  constructor(private userService: UserService) {
    super()
  }

  protected dataProvider(): () => Observable<UserDto[]> {
    return () => this.userService.getAll()
  }

}
