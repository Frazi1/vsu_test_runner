import {Component, Inject, OnInit} from '@angular/core';
import {TestTemplate} from '../../shared/TestTemplate';
import {MockTemplatesService} from '../../services/mock-templates.service';
import {ITemplateService} from "../../services/interfaces";

@Component({
  selector: 'app-test-template-list',
  templateUrl: './test-template-list.component.html',
  styleUrls: ['./test-template-list.component.less']
})
export class TestTemplateListComponent implements OnInit {
  private testTemplates: TestTemplate[];

  constructor(@Inject('ITemplateService') private templatesService: ITemplateService) {
  }

  ngOnInit() {
    this.templatesService.getTemplates().subscribe(res => this.testTemplates = res);
  }
}
