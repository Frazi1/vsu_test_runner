import { Component, Inject, OnDestroy, OnInit } from '@angular/core'
import { TestTemplate } from '../../../shared/TestTemplate'
import { ITemplateService } from '../../../services/interfaces'
import { InstanceService } from '../../../services/instance.service'
import { mergeMap, retry, startWith, takeUntil, tap } from 'rxjs/internal/operators'
import { Observable, Subject } from 'rxjs/index'
import { NgbModal } from '@ng-bootstrap/ng-bootstrap'
import { TestTemplatePermissionsModalComponent } from '../../modals/test-template-permissions-modal/test-template-permissions-modal.component'

@Component({
  selector:    'app-test-template-list',
  templateUrl: './test-template-list.component.html',
  styleUrls:   ['./test-template-list.component.scss']
})
export class TestTemplateListComponent implements OnInit, OnDestroy {
  restore$ = new Subject<number>()
  includeDeleted$ = new Subject<boolean>()

  private _unsubscribe$ = new Subject()

  private _testTemplates$: Observable<TestTemplate[]>
  includeDeleted = false


  constructor(@Inject('ITemplateService') private templatesService: ITemplateService,
              private instanceService: InstanceService,
              private modalService: NgbModal) {
  }

  ngOnInit() {
    this.subscribeToRestore()
    this.subscribeToLoadTemplates()
  }

  public ngOnDestroy(): void {
    this._unsubscribe$.next()
  }

  private subscribeToLoadTemplates(): void {
    this.includeDeleted$.pipe(
      takeUntil(this._unsubscribe$),
      startWith(this.includeDeleted),
      tap(v => console.log(`Include change: ${v}`)),
      tap(v => this._testTemplates$ = this.loadTemplates(v)),
      retry(),
    ).subscribe()
  }

  private subscribeToRestore() {
    this.restore$.pipe(
      takeUntil(this._unsubscribe$),
      tap(id => console.log(`Restoring: ${id}`)),
      mergeMap(id => this.templatesService.restore(id)),
      tap(_ => this._testTemplates$ = this.loadTemplates(this.includeDeleted)),
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

  public openPermissionsModal(templateId: number) {
    const modalRef = this.modalService.open(TestTemplatePermissionsModalComponent)
    modalRef.componentInstance.testTemplateId = templateId
  }
}
