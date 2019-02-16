import {Component, Input, OnInit, Output} from '@angular/core';
import {Function} from '../../../shared/Function';
import {SupportedCodeProviderService} from '../../../services/supported-code-provider.service';
import {CodeType} from '../../../shared/CodeType';
import {FunctionArgument} from '../../../shared/FunctionArgument';

@Component({
  selector: 'app-function-editor',
  templateUrl: './function-editor.component.html',
  styleUrls: ['./function-editor.component.less']
})
export class FunctionEditorComponent implements OnInit {


  constructor(private supportedCodeProviderService: SupportedCodeProviderService) {
  }

  @Input()
  @Output()
  public functionObj: Function;

  private _defaultCodeTypeValue: CodeType = new CodeType('Unset');
  private _codeTypes: CodeType[];

  ngOnInit() {
    console.log(this.functionObj);
    this.supportedCodeProviderService.codeTypes()
      .subscribe(res => this._codeTypes = res);

    if (this.functionObj == null) {
      this.functionObj = new Function();
    }

    if (this.functionObj.returnType == null) {
      this.functionObj.returnType = this._defaultCodeTypeValue;
    }
  }

  private addArgument(): void {
    this.functionObj.arguments.push(new FunctionArgument('', null));
  }

  private deleteArgument(argument: FunctionArgument): void {
    this.functionObj.arguments = this.functionObj.arguments.filter(arg => arg !== argument);
  }
}
