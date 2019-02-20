import {Component, OnInit} from '@angular/core';
import {CodeLanguage} from '../../../shared/CodeLanguage';
import {CodeService} from '../../../services/code.service';
import {BaseSelectorWithDefaultValueComponent} from '../base/BaseSelectorWithDefaultValueComponent';

@Component({
  selector: 'app-code-language-selector',
  templateUrl: './language-selector.component.html',
  styleUrls: ['./language-selector.component.less']
})
export class LanguageSelectorComponent extends BaseSelectorWithDefaultValueComponent<CodeLanguage> implements OnInit {

  protected options: CodeLanguage[];

  constructor(private codeService: CodeService) {
    super(new CodeLanguage('Не задано'));
  }

  async ngOnInit() {
    this.options = await this.codeService.languages().toPromise();
  }
}
