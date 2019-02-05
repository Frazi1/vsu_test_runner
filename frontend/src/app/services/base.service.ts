import {JsonConvert} from 'json2typescript';
import {Config} from '../shared/Config';
import {HttpClient} from '@angular/common/http';

export class BaseService {
  private _endpoint: string;

  get endpoint(): string {
    return this._endpoint;
  }

  constructor(protected http: HttpClient,
              protected config: Config,
              protected json: JsonConvert,
              endpointPostfix: string) {
    this._endpoint = `${this.config.serverUrl}/${endpointPostfix}`;
  }
}
