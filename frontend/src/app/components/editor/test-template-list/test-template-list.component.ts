import { Component, Inject, OnDestroy, OnInit } from '@angular/core'
import { TestTemplate } from '../../../shared/TestTemplate'
import { ITemplateService } from '../../../services/interfaces'
import { InstanceService } from '../../../services/instance.service'
import { mergeMap, startWith, switchMap, tap } from 'rxjs/internal/operators'
import { Observable, Subject } from 'rxjs/index'

@Component({
  selector:    'app-test-template-list',
  templateUrl: './test-template-list.component.html',
  styleUrls:   ['./test-template-list.component.less']
})
export class TestTemplateListComponent implements OnInit, OnDestroy {
  private _restore$ = new Subject<number>()
  private _includeDeleted$ = new Subject<boolean>()

  private testTemplates: TestTemplate[]
  private _includeDeleted = false


  constructor(@Inject('ITemplateService') private templatesService: ITemplateService,
              private instanceService: InstanceService) {
  }

  ngOnInit() {
    this.subscribeToRestore()
    this.subscribeToIncludeDeleted()
  }

  public ngOnDestroy(): void {
    this._restore$.unsubscribe()
    this._includeDeleted$.unsubscribe()
  }

  private subscribeToIncludeDeleted() {
    // noinspection TypeScriptValidateTypes
    this._includeDeleted$.pipe(
      startWith(this._includeDeleted),
      tap(v => console.log(`Include change: ${v}`)),
      mergeMap(v => this.loadTemplates(v)),
      tap(res => this.testTemplates = res)
    ).subscribe()
  }

  private subscribeToRestore() {
    this._restore$.pipe(
      tap(id => console.log(`Restoring: ${id}`)),
      mergeMap(id => this.templatesService.restore(id)),
      switchMap(id => this.loadTemplates(this._includeDeleted)),
      tap(res => this.testTemplates = res)
    ).subscribe()
  }


  private loadTemplates(includeDeleted: boolean): Observable<TestTemplate[]> {
    return this.templatesService.getTemplates(includeDeleted)
  }

  private createTestInstance(templateId: number): void {
    this.instanceService.createTestInstance(templateId)
        .subscribe(res => {
          console.log(`Instance created. ID: ${res}`)
        })
  }
}
