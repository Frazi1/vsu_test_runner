import { BrowserModule } from '@angular/platform-browser'
import { ErrorHandler, NgModule } from '@angular/core'

import { AppRoutingModule } from './app-routing.module'
import { AppComponent } from './app.component'
import { TestTemplateEditorComponent } from './components/editor/test-template-editor/test-template-editor.component'
import { TestQuestionTemplateEditorComponent } from './components/editor/test-question-template-editor/test-question-template-editor.component'
import { FormsModule, ReactiveFormsModule } from '@angular/forms'
import { TestTemplateListComponent } from './components/editor/test-template-list/test-template-list.component'
import { NavMenuComponent } from './nav-menu/nav-menu.component'
import { HTTP_INTERCEPTORS, HttpClient, HttpClientModule } from '@angular/common/http'
import { TemplatesService } from './services/templates.service'
import { FunctionEditorComponent } from './components/editor/function-signature-editor/function-editor.component'
import { CodeTypeSelectorComponent } from './components/editor/code-type-selector/code-type-selector.component'
import { TestInstanceListComponent } from './components/instance/test-instance-list/test-instance-list.component'
import { TestInstanceEditorComponent } from './components/instance/test-instance-editor/test-instance-editor.component'
import { OWL_DATE_TIME_LOCALE, OwlDateTimeModule, OwlNativeDateTimeModule } from 'ng-pick-datetime'
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'
import { ToastrModule } from 'ngx-toastr'
import { GlobalErrorHandler } from './configuration/global-error-handler'
import { TestRunnerComponent } from './components/runner/test-runner/test-runner.component'
import { QuestionRunnerComponent } from './components/runner/question-runner/question-runner.component'
import { TestRunsListComponent } from './components/runner/test-runs-list/test-runs-list.component'
import { CodeEditorComponent } from './code-editor/code-editor.component'
import { LanguageSelectorComponent } from './components/editor/language-selector/language-selector.component'
import { ClassTransformer } from 'class-transformer'
import { ContentTypeInterceptor } from './interceptors/content-type.interceptor'
import { TestResultViewerComponent } from './components/test-result/test-result-viewer/test-result-viewer.component'
import { QuestionAnswerResultViewerComponent } from './components/test-result/answer-result-viewer/question-answer-result-viewer.component'
import { QuestionLinkComponent } from './components/editor/question-link/question-link.component'
import { AnswerIterationsViewerComponent } from './components/test-result/answer-iterations-viewer/answer-iterations-viewer.component'
import { OutputViewerComponent } from './components/output-viewer/output-viewer.component'
import { AngularSplitModule } from 'angular-split'
import { AceConfig, AceConfigInterface, AceModule } from 'ngx-ace-wrapper'
import { MarkdownModule } from 'ngx-markdown'
import { AutosizeModule } from 'ngx-autosize'
import { CodeEditorWithExecutorComponent } from './components/code-editor-with-executor/code-editor-with-executor.component'
import { GeneratorEditorComponent } from './components/generator/generator-editor/generator-editor.component'
import { AuthComponent } from './components/auth/auth.component'
import { AuthenticationInterceptor } from './interceptors/authentication.interceptor'
import { LogoutComponent } from './components/logout/logout.component'
import { GeneratorRunnerComponent } from './components/generator/generator-runner/generator-runner.component'
import { GeneratorListComponent } from './components/generator/generator-list/generator-list.component'
import { GeneratorListModalComponent } from './components/generator/generator-list-modal/generator-list-modal.component'
import { NgbModalModule, NgbModule } from '@ng-bootstrap/ng-bootstrap'
import { ModalOkCancelComponent } from './components/modals/modal-ok-cancel/modal-ok-cancel.component'
import { GeneratorRunnerModalComponent } from './components/generator/generator-runner-modal/generator-runner-modal.component'
import { GroupManagementComponent } from './components/management/group-management/group-management.component'
import { ManagementComponent } from './components/management/management/management.component'
import { GroupEditorComponent } from './components/editor/group-editor/group-editor.component'
import { TreeModule } from 'angular-tree-component'
import { GroupsUsersSelectorComponent } from './components/management/groups-users-selector/groups-users-selector.component'
import { AssigneeEditorComponent } from './components/management/permissions-editor/assignee-editor.component'
import { UserListComponent } from './components/management/user-list/user-list.component'
import { TestTemplatePermissionsEditorComponent } from './components/management/test-permissions-editor/test-template-permissions-editor.component'
import { TestTemplatePermissionsModalComponent } from './components/modals/test-template-permissions-modal/test-template-permissions-modal.component'
import { ModalCloseOnlyComponent } from './components/modals/modal-close-only/modal-close-only.component'
import { ActiveDirectoryQueryComponent } from './components/management/active-directory-query/active-directory-query.component'
import { ActiveDirectoryUsersSelectorComponent } from './components/management/active-directory-users-selector/active-directory-users-selector.component'
import { QuestionListComponent } from './components/question-list/question-list.component';
import { QuestionBankListComponent } from './components/question-bank/question-bank-list/question-bank-list.component';
import { QuestionBankQuestionEditorComponent } from './components/question-bank/question-bank-question-editor/question-bank-question-editor.component';
import { SectionSelectorComponent } from './components/question-bank/section-selector/section-selector.component'

const DEFAULT_ACE_CONFIG: AceConfigInterface = {}

@NgModule({
  declarations:    [
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
    TestResultViewerComponent,
    QuestionAnswerResultViewerComponent,
    QuestionLinkComponent,
    AnswerIterationsViewerComponent,
    OutputViewerComponent,
    CodeEditorWithExecutorComponent,
    GeneratorEditorComponent,
    AuthComponent,
    LogoutComponent,
    GeneratorRunnerComponent,
    GeneratorListComponent,
    GeneratorListModalComponent,
    ModalOkCancelComponent,
    GeneratorRunnerModalComponent,
    GroupManagementComponent,
    ManagementComponent,
    GroupEditorComponent,
    GroupsUsersSelectorComponent,
    AssigneeEditorComponent,
    UserListComponent,
    TestTemplatePermissionsEditorComponent,
    TestTemplatePermissionsModalComponent,
    ModalCloseOnlyComponent,
    ActiveDirectoryQueryComponent,
    ActiveDirectoryUsersSelectorComponent,
    QuestionListComponent,
    QuestionBankListComponent,
    QuestionBankQuestionEditorComponent,
    SectionSelectorComponent,
  ],
  imports:         [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    FormsModule,
    OwlDateTimeModule,
    OwlNativeDateTimeModule,
    BrowserAnimationsModule,
    ToastrModule.forRoot(),
    AngularSplitModule.forRoot(),
    AceModule,
    MarkdownModule.forRoot({loader: HttpClient}),
    AutosizeModule,
    ReactiveFormsModule,
    NgbModalModule,
    NgbModule,
    // TreeviewModule.forRoot(),
    TreeModule.forRoot()
  ],
  providers:       [
    {provide: 'ITemplateService', useClass: TemplatesService},
    // {provide: JsonConvert, useValue: jsonConvert},
    {provide: ClassTransformer, useValue: new ClassTransformer()},
    {provide: ErrorHandler, useClass: GlobalErrorHandler},
    {
      provide:  HTTP_INTERCEPTORS,
      useClass: ContentTypeInterceptor,
      multi:    true
    },
    {
      provide:  HTTP_INTERCEPTORS,
      useClass: AuthenticationInterceptor,
      multi:    true
    },
    {provide: AceConfig, useValue: DEFAULT_ACE_CONFIG},
    {provide: OWL_DATE_TIME_LOCALE, useValue: 'ru'}
  ],
  bootstrap:       [AppComponent],
  entryComponents: [
    GeneratorListModalComponent,
    GeneratorRunnerModalComponent,
    TestTemplatePermissionsModalComponent
  ],
})
export class AppModule {
}
