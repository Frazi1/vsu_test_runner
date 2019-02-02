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
import {FunctionEditorComponent} from './editor/function-signature-editor/function-editor.component';
import {CodeTypeSelectorComponent} from './editor/code-type-selector/code-type-selector.component';
import {JsonConvert} from 'json2typescript';
import {jsonConvert} from './configuration/JsonConfiguration';
import {TestInstanceListComponent} from './components/instance/test-instance-list/test-instance-list.component';
import {TestInstanceEditorComponent} from './components/instance/test-instance-editor/test-instance-editor.component';
import {OwlDateTimeModule, OwlNativeDateTimeModule} from 'ng-pick-datetime';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

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
    TestInstanceEditorComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    FormsModule,
    OwlDateTimeModule,
    OwlNativeDateTimeModule,
    BrowserAnimationsModule,
  ],
  providers: [
    {provide: 'ITemplateService', useClass: TemplatesService},
    {provide: JsonConvert, useValue: jsonConvert}
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
