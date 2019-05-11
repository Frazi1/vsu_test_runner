import { Component, Input, OnDestroy, OnInit } from '@angular/core'
import { Observable, Subject } from 'rxjs'
import { takeUntil } from 'rxjs/operators'
import { CodeExecutionResponseDto } from '../../shared/runner/CodeExecutionResponseDto'

@Component({
  selector:    'app-output-viewer',
  templateUrl: './output-viewer.component.html',
  styleUrls:   ['./output-viewer.component.less']
})
export class OutputViewerComponent implements OnDestroy {

  private _textSource$: Observable<CodeExecutionResponseDto>
  private _unsubscribe$ = new Subject<void>()

  detailedItem: CodeExecutionResponseDto
  responses: CodeExecutionResponseDto[] = []

  @Input()
  set textSource(value: Observable<CodeExecutionResponseDto>) {
    this._unsubscribe$.next()
    this._textSource$ = value
    if (this._textSource$ != null) {
      this._textSource$.pipe(
        takeUntil(this._unsubscribe$)
      ).subscribe(resp => this.append(resp))
    }
  }

  public ngOnDestroy(): void {
    this._unsubscribe$.next()
  }

  private append(response: CodeExecutionResponseDto): void {
    this.responses.push(response)
  }

  public clear(): void {
    this.responses.length = 0
  }

  public setDetailedItem(bubble: CodeExecutionResponseDto) {
    this.detailedItem = bubble
  }
}
