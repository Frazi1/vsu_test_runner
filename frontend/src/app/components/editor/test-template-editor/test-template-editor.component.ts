import { Component, Inject, OnInit, Output } from '@angular/core'
import { ActivatedRoute, Router } from '@angular/router'
import { Subscription } from 'rxjs/index'
import { TestTemplate } from '../../../shared/TestTemplate'
import { TestQuestionTemplate } from '../../../shared/TestQuestionTemplate'
import { ITemplateService } from '../../../services/interfaces'

@Component({
  selector:    'app-test-template-editor',
  templateUrl: './test-template-editor.component.html',
  styleUrls:   ['./test-template-editor.component.less']
})
export class TestTemplateEditorComponent implements OnInit {

  @Output()
  private testTemplate: TestTemplate
  private paramSubscription: Subscription
  private isCreating: boolean

  constructor(private route: ActivatedRoute,
              @Inject('ITemplateService') private templatesService: ITemplateService,
              private router: Router) {
  }

  ngOnInit() {
    this.paramSubscription = this.route.params.subscribe(params => {
      const id = params['id']
      if (!id) {
        this.isCreating = true
        this.testTemplate = new TestTemplate()
      } else {
        this.isCreating = false
        this.templatesService.getTemplate(+id).subscribe(res => this.testTemplate = res)
      }
    })
  }

  private addQuestion(): void {
    this.testTemplate.questionTemplates.push(new TestQuestionTemplate())
  }

  private removeQuestion(q: TestQuestionTemplate) {
    this.testTemplate.questionTemplates = this.testTemplate.questionTemplates.filter(i => i !== q)
  }

  private save(): void {
    if (this.isCreating) {
      this.add()
    } else {
      this.update()
    }
  }

  private add(): void {
    this.templatesService.addTemplate(this.testTemplate)
        .subscribe(id => this.router.navigate(['/template', id]))
  }

  private update(): void {
    this.templatesService.updateTemplate(this.testTemplate)
        .subscribe(id => this.templatesService.getTemplate(+id).subscribe(res => this.testTemplate = res))
  }

  private deleteTemplate(): void {
    if (this.isCreating === false) {
      this.templatesService.deleteTemplate(this.testTemplate.id)
          .subscribe(() => this.router.navigate(['/']))
    }
  }
}
