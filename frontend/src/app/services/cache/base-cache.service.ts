import { merge, Observable, Subject, timer } from 'rxjs'
import { retry, shareReplay, switchMap, tap } from 'rxjs/operators'

export abstract class BaseCacheService<T> {
  private CACHE_REFRESH_INTERVAL = 10 * 1000 * 10 // 10 minutes

  protected _cache: Observable<T>
  protected _invalidate$ = new Subject()
  protected _invalidateSuccess$ = new Subject()


  private createTimerCache(dataProvider: () => Observable<T>) {
    const timer$ = timer(0, this.CACHE_REFRESH_INTERVAL)
    const cache$ = merge(timer$, this._invalidate$).pipe(
      switchMap(dataProvider),
      tap(() => this._invalidateSuccess$.next()),
      retry(),
      shareReplay(1)
    )
    return cache$
  }

  public invalidate(): Observable<any> {
    if (this.ensureCacheExists()) {
      this._invalidate$.next()
    }
    return this._invalidateSuccess$.asObservable()
  }


  protected abstract dataProvider(): () => Observable<T>

  public getCached(force = false): Observable<T> {
    if (this.ensureCacheExists() && force) {
      return this.invalidate().pipe(
        switchMap(() => this._cache)
      )
    }
    return this._cache
  }


  private ensureCacheExists(): boolean {
    if (!this._cache) {
      this._cache = this.createTimerCache(this.dataProvider())
      return false
    }
    return true
  }
}
