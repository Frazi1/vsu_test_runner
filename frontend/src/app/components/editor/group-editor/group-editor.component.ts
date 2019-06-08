import { Component, Input, OnInit } from '@angular/core'
import { GroupDto } from '../../../shared/GroupDto'
import { ActivatedRoute, Router } from '@angular/router'
import { mergeMap, retry, switchMap, takeUntil, tap } from 'rxjs/operators'
import { Observable, of, Subject } from 'rxjs'
import { GroupCacheService } from '../../../services/cache/group-cache.service'
import { BaseComponent } from '../../base.component'
import { GroupService } from '../../../services/group.service'
import { Location } from '@angular/common'

@Component({
  selector:    'app-group-editor',
  templateUrl: './group-editor.component.html',
  styleUrls:   ['./group-editor.component.scss']
})
export class GroupEditorComponent extends BaseComponent implements OnInit {

  @Input()
  group: GroupDto

  allGroups$: Observable<GroupDto[]>

  mainBtn$ = new Subject()
  isCreating = true

  constructor(private activatedRoute: ActivatedRoute,
              private groupCache: GroupCacheService,
              private groupService: GroupService,
              private location: Location) {
    super()
  }

  ngOnInit() {
    this.group = new GroupDto()
    this.allGroups$ = this.groupCache.groups
    this.initSub()

    this.mainBtnSub()
  }

  private mainBtnSub() {
    this.mainBtn$.pipe(
      takeUntil(this.onDestroy$),
      retry(),
      switchMap(() => this.groupService.addGroup(this.group)),
      switchMap(() => this.groupCache.invalidate()),
      tap(() => this.location.back())
    ).subscribe()
  }

  private initSub() {
    this.activatedRoute.params.pipe(
      switchMap(params => {
        let parentId = params['parentId']
        return parentId != null ? of(+parentId) : of()
      }),
      tap(parentId => this.group.parentGroupId = parentId),
      switchMap(() => this.allGroups$),
      tap(groups => this.group.parentGroup = groups.find(g => g.id === this.group.parentGroupId))
    ).subscribe()
  }
}
