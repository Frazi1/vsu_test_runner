import {Component, Inject, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {Subscription} from 'rxjs/index';
import {TestTemplate} from '../../shared/TestTemplate';
import {TestQuestionTemplate} from '../../shared/TestQuestionTemplate';
import {MockTemplatesService} from '../../services/mock-templates.service';
import {ITemplateService} from "../../services/interfaces";

@Component({
  selector: 'app-test-template-editor',
  templateUrl: './test-template-editor.component.html',
  styleUrls: ['./test-template-editor.component.less']
})
export class TestTemplateEditorComponent implements OnInit {

  private testTemplate: TestTemplate;
  private paramSubscription: Subscription;

  constructor(private route: ActivatedRoute,
              @Inject('ITemplateService') private templatesService: ITemplateService,
              private router: Router) {
  }

  ngOnInit() {
    this.paramSubscription = this.route.params.subscribe(params => {
      const id = params['id'];
      if (!id) {
        this.testTemplate = new TestTemplate();
      } else {
        this.templatesService.getTemplate(+id).subscribe(res => this.testTemplate = res);
      }
    });
  }

  private addQuestion(): void {
    this.testTemplate.questionTemplates.push(new TestQuestionTemplate());
  }

  private save(): void {
    this.templatesService.addTemplate(this.testTemplate)
      .subscribe(id => this.router.navigate(['/template', id]));
  }
}
