import { Observable, Subject } from 'rxjs'
import { debounceTime, distinctUntilChanged, switchMap, take } from 'rxjs/operators'
import { AbstractControl } from '@angular/forms'

export class AsyncValidatorDebouncedValidator {
  input$ = new Subject<any>()
  chain$: Observable<any>


  constructor(validatorProvider: (value: any) => Observable<any>) {
    this.chain$ = this.input$.pipe(
      debounceTime(500),
      distinctUntilChanged(),
      switchMap(validatorProvider),
      take(1)
    )
  }

  validate = (control: AbstractControl) => {
    setTimeout(() => this.input$.next(control.value), 0)
    return this.chain$
  }
}
