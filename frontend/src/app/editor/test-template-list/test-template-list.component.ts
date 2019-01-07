import {Component, Inject, OnInit} from '@angular/core';
import {TestTemplate} from '../../shared/TestTemplate';
import {TemplatesService} from '../../services/templates.service';

@Component({
  selector: 'app-test-template-list',
  templateUrl: './test-template-list.component.html',
  styleUrls: ['./test-template-list.component.less']
})
export class TestTemplateListComponent implements OnInit {
  private testTemplates: TestTemplate[];

  constructor(@Inject(TemplatesService) private templatesService) {
  }

  ngOnInit() {
    this.templatesService.getTemplates().subscribe(res => this.testTemplates = res);
  }
}
