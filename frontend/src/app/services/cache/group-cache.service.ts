import { Injectable } from '@angular/core'
import { merge, Observable, Subject, timer } from 'rxjs'
import { GroupDto } from '../../shared/GroupDto'
import { map, shareReplay, switchMap, tap } from 'rxjs/operators'
import { GroupService } from '../group.service'
import { GroupsHelper } from '../../utils/GroupsHelper'

@Injectable({
  providedIn: 'root'
})
export class GroupCacheService {
  private CACHE_REFRESH_INTERVAL = 10 * 1000 * 10 // 10 minutes
  private _groupCache$: Observable<GroupDto[]>
  private _invalidate$ = new Subject()
  private _invalidateSuccess$ = new Subject()

  constructor(private groupService: GroupService) { }

  private createTimerCache<T>(dataProvider: () => Observable<T>) {
    const timer$ = timer(0, this.CACHE_REFRESH_INTERVAL)
    const cache$ = merge(timer$, this._invalidate$).pipe(
      switchMap(dataProvider),
      tap(() => this._invalidateSuccess$.next()),
      shareReplay(1)
    )
    return cache$
  }

  public get groups(): Observable<GroupDto[]> {
    if (!this._groupCache$) {
      this._groupCache$ = this.createTimerCache(
        () => this.groupService.getAll()
                  .pipe(
                    map(groups => {
                      GroupsHelper.setGroupRelations(groups)
                      return groups
                    })
                  )
      )
    }
    return this._groupCache$
  }

  public invalidate(): Observable<any> {
    this._invalidate$.next()
    return this._invalidateSuccess$
  }
}
