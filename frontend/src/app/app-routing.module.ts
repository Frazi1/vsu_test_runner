import { NgModule } from '@angular/core'
import { RouterModule, Routes } from '@angular/router'
import { TestTemplateEditorComponent } from './components/editor/test-template-editor/test-template-editor.component'
import { TestTemplateListComponent } from './components/editor/test-template-list/test-template-list.component'
import { TestInstanceListComponent } from './components/instance/test-instance-list/test-instance-list.component'
import { TestInstanceEditorComponent } from './components/instance/test-instance-editor/test-instance-editor.component'
import { TestRunnerComponent } from './components/runner/test-runner/test-runner.component'
import { TestRunsListComponent } from './components/runner/test-runs-list/test-runs-list.component'
import { TestResultViewerComponent } from './components/test-result/test-result-viewer/test-result-viewer.component'
import { GeneratorEditorComponent } from './components/generator/generator-editor/generator-editor.component'
import { AuthComponent } from './components/auth/auth.component'
import { AuthGuard } from './configuration/auth.guard'
import { LogoutComponent } from './components/logout/logout.component'
import { GeneratorListComponent } from './components/generator/generator-list/generator-list.component'
import { ManagementComponent } from './components/management/management/management.component'
import { GroupEditorComponent } from './components/editor/group-editor/group-editor.component'

const routes: Routes = [
  {path: 'auth', component: AuthComponent, data: {isSignUp: false}},
  {path: 'auth/signup', component: AuthComponent, data: {isSignUp: true}},
  {
    path: '', canActivate: [AuthGuard], canActivateChild: [AuthGuard], children: [
      {path: 'template/new', component: TestTemplateEditorComponent},
      {path: 'template/:id', component: TestTemplateEditorComponent},
      {path: 'template', component: TestTemplateListComponent},
      {path: 'instance', component: TestInstanceListComponent},
      {path: 'instance/:id', component: TestInstanceEditorComponent},
      {path: 'run/:id', component: TestRunnerComponent},
      {path: 'run', component: TestRunsListComponent},
      {path: 'result/:id', component: TestResultViewerComponent},
      {
        path: 'generator', children: [
          {path: '', component: GeneratorListComponent},
          {path: 'new', component: GeneratorEditorComponent},
          {path: ':id', component: GeneratorEditorComponent},
        ]
      },
      {
        path: 'management', children: [
          {path: '', component: ManagementComponent},
          {
            path: 'group', children: [
              {path: 'new', component: GroupEditorComponent},
              {path: 'new/:id', component: GroupEditorComponent}
            ]
          }
        ]
      },
      {path: 'logout', component: LogoutComponent}
    ]
  }

]

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
