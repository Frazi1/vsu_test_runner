import { OnDestroy } from '@angular/core'
import { Observable, Subject } from 'rxjs'
import { retry, takeUntil } from 'rxjs/operators'

export class BaseComponent implements OnDestroy {
  protected onDestroy$ = new Subject()

  protected createGuardedObservable<T>(source: Observable<T>): Observable<T> {
    return source.pipe(
      takeUntil(this.onDestroy$)
    )
  }

  public ngOnDestroy(): void {
    this.onDestroy$.next()
  }

}
