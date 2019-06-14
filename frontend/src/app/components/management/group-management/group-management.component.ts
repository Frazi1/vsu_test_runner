import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { BaseComponent } from '../../base.component'
import { GroupDto } from '../../../shared/GroupDto'
import { Observable, of } from 'rxjs'
import { map, switchMap} from 'rxjs/operators'
import { ITreeNode } from 'angular-tree-component/dist/defs/api'

@Component({
  selector:    'app-group-management',
  templateUrl: './group-management.component.html',
  styleUrls:   ['./group-management.component.scss']
})
export class GroupManagementComponent extends BaseComponent implements OnInit {

  @Input()
  groups: Observable<GroupDto[]>

  nodes$: Observable<any[]>

  @Output()
  selectedGroupChange = new EventEmitter<GroupDto>()

  constructor() {
    super()
  }

  ngOnInit() {
    this.nodes$ = this.createTreeNodes(this.groups)
  }

  selectionChange(node: ITreeNode) {
    this.selectedGroupChange.emit(node.data)
  }

  private createTreeNodes(groupsObs: Observable<GroupDto[]>) {
    return groupsObs.pipe(
      switchMap(groups => of(groups.filter(g => g.parentGroupId == null))),
      map(groups => groups.map(g => this.createTreeNodeFromGroup(g)))
    )
  }

  private createTreeNodeFromGroup(group: GroupDto): any {
    return {
      id:       group.id,
      name:     group.name,
      value:    group,
      children: group.childrenGroups.map(g => this.createTreeNodeFromGroup(g))
    }
  }
}
