import { Component, OnInit } from '@angular/core'
import { CodeType } from '../../../shared/CodeType'
import { CodeService } from '../../../services/code.service'
import { BaseSelectorWithDefaultValueComponent } from '../base/BaseSelectorWithDefaultValueComponent'
import { Observable } from 'rxjs/index'

@Component({
  selector:    'app-code-type-selector',
  templateUrl: './code-type-selector.component.html',
  styleUrls:   ['./code-type-selector.component.scss']
})
export class CodeTypeSelectorComponent extends BaseSelectorWithDefaultValueComponent<CodeType> implements OnInit {

  protected options: Observable<CodeType[]>

  constructor(private supportedCodeProviderService: CodeService) {
    super(new CodeType('Не задано'))
  }

  ngOnInit() {
    this.options = this.supportedCodeProviderService.codeTypes()
  }
}
