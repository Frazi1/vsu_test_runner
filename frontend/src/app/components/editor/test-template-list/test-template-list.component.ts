import { Component, Inject, OnInit } from '@angular/core'
import { TestTemplate } from '../../../shared/TestTemplate'
import { ITemplateService } from '../../../services/interfaces'
import { InstanceService } from '../../../services/instance.service'

@Component({
  selector:    'app-test-template-list',
  templateUrl: './test-template-list.component.html',
  styleUrls:   ['./test-template-list.component.less']
})
export class TestTemplateListComponent implements OnInit {
  private testTemplates: TestTemplate[]

  constructor(@Inject('ITemplateService') private templatesService: ITemplateService,
              private instanceService: InstanceService) {
  }

  ngOnInit() {
    this.templatesService.getTemplates().subscribe(res => this.testTemplates = res)
  }

  private createTestInstance(templateId: number): void {
    this.instanceService.createTestInstance(templateId)
        .subscribe(res => {
          console.log(`Instance created. ID: ${res}`)
        })
  }
}
