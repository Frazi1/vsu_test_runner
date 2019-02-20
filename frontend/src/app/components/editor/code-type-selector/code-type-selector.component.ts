import {ChangeDetectorRef, Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {CodeType} from '../../../shared/CodeType';
import {CodeService} from '../../../services/code.service';
import {BaseSelectorWithDefaultValueComponent} from '../base/BaseSelectorWithDefaultValueComponent';

@Component({
  selector: 'app-code-type-selector',
  templateUrl: './code-type-selector.component.html',
  styleUrls: ['./code-type-selector.component.less']
})
export class CodeTypeSelectorComponent extends BaseSelectorWithDefaultValueComponent<CodeType> implements OnInit {

  protected options: CodeType[];

  constructor(private supportedCodeProviderService: CodeService) {
    super(new CodeType('Не задано'));
  }

  ngOnInit() {
    this.supportedCodeProviderService.codeTypes()
      .subscribe(res => {
        this.options = res;
        if (this.value == null) {
          this.value = this.defaultValue;
        }
      });
  }
}
