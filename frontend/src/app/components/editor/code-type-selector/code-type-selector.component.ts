import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {CodeType} from '../../../shared/CodeType';
import {CodeService} from '../../../services/code.service';

@Component({
  selector: 'app-code-type-selector',
  templateUrl: './code-type-selector.component.html',
  styleUrls: ['./code-type-selector.component.less']
})
export class CodeTypeSelectorComponent implements OnInit {

  private _codeTypes: CodeType[];
  private _defaultCodeTypeValue: CodeType = new CodeType('Not set');

  @Input() public isReadOnly = false;

  @Input() public value: CodeType;

  @Output() public valueChange = new EventEmitter<CodeType>();

  constructor(private supportedCodeProviderService: CodeService) {
    this.codeTypeComparer = this.codeTypeComparer.bind(this);
  }

  private codeTypeComparer(a: CodeType, b: CodeType): boolean {
    if (a != null && b != null) {
      return a.name === b.name;
    }
    if (a === this._defaultCodeTypeValue && b == null) {
      return true;
    }
    if (b === this._defaultCodeTypeValue && a == null) {
      return true;
    }

    // noinspection TsLint
    return a == b;
  }

  ngOnInit() {
    this.supportedCodeProviderService.codeTypes()
      .subscribe(res => {
        this._codeTypes = res;
        if (this.value == null) {
          this.value = this._defaultCodeTypeValue;
        }
      });
  }

  onValueChange($event: Event, val) {
    console.log(`Change event: ${$event}`);
    console.log(`Val: ${val.name}`);
    this.valueChange.emit(val);
  }
}
