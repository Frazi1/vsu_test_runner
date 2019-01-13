import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppRoutingModule} from './app-routing.module';
import {AppComponent} from './app.component';
import {TestTemplateEditorComponent} from './editor/test-template-editor/test-template-editor.component';
import {TestQuestionTemplateEditorComponent} from './editor/test-question-template-editor/test-question-template-editor.component';
import {FormsModule} from '@angular/forms';
import {TestTemplateListComponent} from './editor/test-template-list/test-template-list.component';
import {NavMenuComponent} from './nav-menu/nav-menu.component';
import {HttpClientModule} from '@angular/common/http';
import {TemplatesService} from './services/templates.service';

@NgModule({
  declarations: [
    AppComponent,
    TestTemplateEditorComponent,
    TestQuestionTemplateEditorComponent,
    TestTemplateListComponent,
    NavMenuComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    FormsModule
  ],
  providers: [{provide: 'ITemplateService', useClass: TemplatesService}],
  bootstrap: [AppComponent]
})
export class AppModule {
}
