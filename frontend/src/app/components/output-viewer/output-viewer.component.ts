import { Component, Input, OnDestroy, OnInit } from '@angular/core'
import { Observable, Subject } from 'rxjs'
import { takeUntil } from 'rxjs/operators'

@Component({
  selector:    'app-output-viewer',
  templateUrl: './output-viewer.component.html',
  styleUrls:   ['./output-viewer.component.less']
})
export class OutputViewerComponent implements OnInit, OnDestroy {

  outputText: string

  private _textSource$: Observable<string>
  private _unsubscribe$ = new Subject<void>()

  @Input()
  set textSource(value: Observable<string>) {
    this._unsubscribe$.next()
    this._textSource$ = value
    if (this._textSource$ != null) {
      this._textSource$.pipe(
        takeUntil(this._unsubscribe$)
      ).subscribe(msg => this.append(msg))
    }
  }

  constructor() { }

  ngOnInit() {
  }

  public ngOnDestroy(): void {
    this._unsubscribe$.next()
  }

  private append(msg: string): void {
    this.outputText += '\n' + msg
  }

  public clear(): void {
    this.outputText = ''
  }

}
