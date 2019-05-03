import { BrowserModule } from '@angular/platform-browser'
import { ErrorHandler, NgModule } from '@angular/core'

import { AppRoutingModule } from './app-routing.module'
import { AppComponent } from './app.component'
import { TestTemplateEditorComponent } from './components/editor/test-template-editor/test-template-editor.component'
import { TestQuestionTemplateEditorComponent } from './components/editor/test-question-template-editor/test-question-template-editor.component'
import { FormsModule } from '@angular/forms'
import { TestTemplateListComponent } from './components/editor/test-template-list/test-template-list.component'
import { NavMenuComponent } from './nav-menu/nav-menu.component'
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http'
import { TemplatesService } from './services/templates.service'
import { FunctionEditorComponent } from './components/editor/function-signature-editor/function-editor.component'
import { CodeTypeSelectorComponent } from './components/editor/code-type-selector/code-type-selector.component'
import { TestInstanceListComponent } from './components/instance/test-instance-list/test-instance-list.component'
import { TestInstanceEditorComponent } from './components/instance/test-instance-editor/test-instance-editor.component'
import { OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime'
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'
import { ToastrModule } from 'ngx-toastr'
import { GlobalErrorHandler } from './configuration/global-error-handler'
import { TestRunnerComponent } from './components/runner/test-runner/test-runner.component'
import { QuestionRunnerComponent } from './components/runner/question-runner/question-runner.component'
import { TestRunsListComponent } from './components/runner/test-runs-list/test-runs-list.component'
import { CodeEditorComponent } from './code-editor/code-editor.component'
import { LanguageSelectorComponent } from './components/editor/language-selector/language-selector.component'
import { FunctionDeclarativeInputEditorComponent } from './components/editor/function-declarative-input-editor/function-declarative-input-editor.component'
import { ClassTransformer } from 'class-transformer'
import { ContentTypeInterceptor } from './interceptors/content-type.interceptor'
import { TestResultViewerComponent } from './components/test-result/test-result-viewer/test-result-viewer.component'
import { QuestionAnswerResultViewerComponent } from './components/test-result/answer-result-viewer/question-answer-result-viewer.component'
import { QuestionLinkComponent } from './components/editor/question-link/question-link.component';
import { AnswerIterationsViewerComponent } from './components/test-result/answer-iterations-viewer/answer-iterations-viewer.component';
import { OutputViewerComponent } from './components/output-viewer/output-viewer.component'
import { AngularSplitModule } from 'angular-split'

@NgModule({
  declarations: [
    AppComponent,
    TestTemplateEditorComponent,
    TestQuestionTemplateEditorComponent,
    TestTemplateListComponent,
    NavMenuComponent,
    FunctionEditorComponent,
    CodeTypeSelectorComponent,
    TestInstanceListComponent,
    TestInstanceEditorComponent,
    TestRunnerComponent,
    QuestionRunnerComponent,
    TestRunsListComponent,
    CodeEditorComponent,
    LanguageSelectorComponent,
    FunctionDeclarativeInputEditorComponent,
    TestResultViewerComponent,
    QuestionAnswerResultViewerComponent,
    QuestionLinkComponent,
    AnswerIterationsViewerComponent,
    OutputViewerComponent
  ],
  imports:      [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    FormsModule,
    OwlDateTimeModule,
    OwlNativeDateTimeModule,
    BrowserAnimationsModule,
    ToastrModule.forRoot(),
    AngularSplitModule.forRoot()
  ],
  providers:    [
    {provide: 'ITemplateService', useClass: TemplatesService},
    // {provide: JsonConvert, useValue: jsonConvert},
    {provide: ClassTransformer, useValue: new ClassTransformer()},
    {provide: ErrorHandler, useClass: GlobalErrorHandler},
    {
      provide:  HTTP_INTERCEPTORS,
      useClass: ContentTypeInterceptor,
      multi:    true
    }
  ],
  bootstrap:    [AppComponent]
})
export class AppModule {
}
