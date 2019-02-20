import {EventEmitter, Input, Output} from '@angular/core';

export abstract class BaseSelectorWithDefaultValueComponent<T extends { 'name' }> {
  protected defaultValue: T;
  protected abstract options: T[];

  @Input() public isReadOnly = false;

  private _value: T;


  get value(): T {
    return this._value || this.defaultValue;
  }

  @Input()
  set value(v: T) {
    this._value = v;
  }

  @Output() public valueChange = new EventEmitter<T>();

  protected constructor(defaultValue: T) {
    this.defaultValue = defaultValue;
    this.valueComparer = this.valueComparer.bind(this);
  }

  protected valueComparer(a: T, b: T): boolean {
    if (a != null && b != null) {
      return a.name === b.name;
    }
    if (a === this.defaultValue && b == null) {
      return true;
    }
    if (b === this.defaultValue && a == null) {
      return true;
    }

    // noinspection TsLint
    return a == b;
  }

  protected onValueChange($event: Event, val: T) {
    console.log(`Change event: ${$event}`);
    console.log(`Val: ${val.name}`);
    this.valueChange.emit(val);
  }
}
