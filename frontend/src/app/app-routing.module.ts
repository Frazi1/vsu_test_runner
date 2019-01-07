import {NgModule} from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {TestTemplateEditorComponent} from './editor/test-template-editor/test-template-editor.component';
import {TestTemplateListComponent} from './editor/test-template-list/test-template-list.component';

const routes: Routes = [
  {path: 'template/new', component: TestTemplateEditorComponent},
  {path: 'template/:id', component: TestTemplateEditorComponent},
  {path: 'template', component: TestTemplateListComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
