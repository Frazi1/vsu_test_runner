import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {TestTemplateEditorComponent} from './editor/test-template-editor/test-template-editor.component';
import {TestQuestionTemplateEditorComponent} from './editor/test-question-template-editor/test-question-template-editor.component';
import {FormsModule} from '@angular/forms';
import { TestTemplateListComponent } from './editor/test-template-list/test-template-list.component';

@NgModule({
  declarations: [
    AppComponent,
    TestTemplateEditorComponent,
    TestQuestionTemplateEditorComponent,
    TestTemplateListComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
