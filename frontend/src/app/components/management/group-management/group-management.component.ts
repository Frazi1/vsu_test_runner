import { Component, Input, OnInit } from '@angular/core'
import { BaseComponent } from '../../base.component'
import { GroupDto } from '../../../shared/GroupDto'
import { TreeviewConfig, TreeviewItem } from 'ngx-treeview'

@Component({
  selector:    'app-group-management',
  templateUrl: './group-management.component.html',
  styleUrls:   ['./group-management.component.scss']
})
export class GroupManagementComponent extends BaseComponent implements OnInit {

  @Input()
  groups: GroupDto[]

  items: TreeviewItem[]
  treeConfig = TreeviewConfig.create({
    hasCollapseExpand: true,
    hasAllCheckBox: true,
    decoupleChildFromParent: false,
    maxHeight: 400,
    hasFilter: true
  })

  constructor() {
    super()
  }

  ngOnInit() {
    this.items = this.createTreeViewItems(this.groups)
  }

  private createTreeViewItems(groups: GroupDto[]): TreeviewItem[] {
    return groups
      .filter(g => g.parentGroupId == null)
      .map(g => this.createTreeViewItemFromGroup(g))
  }

  private createTreeViewItemFromGroup = (group: GroupDto): TreeviewItem => {
    return new TreeviewItem({
      value:    group,
      text:     group.name || '',
      children: group.childrenGroups.map(this.createTreeViewItemFromGroup),
      collapsed: true
    })
  }


}
