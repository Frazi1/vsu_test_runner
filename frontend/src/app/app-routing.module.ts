import {NgModule} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {TestTemplateEditorComponent} from './components/editor/test-template-editor/test-template-editor.component';
import {TestTemplateListComponent} from './components/editor/test-template-list/test-template-list.component';
import {TestInstanceListComponent} from './components/instance/test-instance-list/test-instance-list.component';
import {TestInstanceEditorComponent} from './components/instance/test-instance-editor/test-instance-editor.component';
import {TestRunnerComponent} from './components/runner/test-runner/test-runner.component';

const routes: Routes = [
  {path: 'template/new', component: TestTemplateEditorComponent},
  {path: 'template/:id', component: TestTemplateEditorComponent},
  {path: 'template', component: TestTemplateListComponent},
  {path: 'instance', component: TestInstanceListComponent},
  {path: 'instance/:id', component: TestInstanceEditorComponent},
  {path: 'run/:id', component: TestRunnerComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
