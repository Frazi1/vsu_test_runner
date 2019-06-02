import { Component, Inject, OnInit, Output, QueryList, ViewChildren } from '@angular/core'
import { ActivatedRoute, Router } from '@angular/router'
import { Subscription } from 'rxjs'
import { TestTemplate } from '../../../shared/TestTemplate'
import { TestQuestionTemplate } from '../../../shared/TestQuestionTemplate'
import { ITemplateService } from '../../../services/interfaces'
import { TestQuestionTemplateEditorComponent } from '../test-question-template-editor/test-question-template-editor.component'
import { switchMap } from 'rxjs/operators'

@Component({
  selector:    'app-test-template-editor',
  templateUrl: './test-template-editor.component.html',
  styleUrls:   ['./test-template-editor.component.scss']
})
export class TestTemplateEditorComponent implements OnInit {

  @Output()
  testTemplate: TestTemplate
  private paramSubscription: Subscription
  private isCreating: boolean

  @ViewChildren(TestQuestionTemplateEditorComponent)
  private questionEditorComponents: QueryList<TestQuestionTemplateEditorComponent>

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
    this.onSave()
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
    const templateId = this.testTemplate.id
    this.templatesService.updateTemplate(this.testTemplate).pipe(
      switchMap(() => this.templatesService.getTemplate(templateId))
    ).subscribe(res => this.testTemplate = res)
  }

  private deleteTemplate(): void {
    if (this.isCreating === false) {
      this.templatesService.deleteTemplate(this.testTemplate.id)
          .subscribe(() => this.router.navigate(['/']))
    }
  }

  public onSave(): void {
    this.questionEditorComponents.forEach(qe => qe.onSave())
  }
}
