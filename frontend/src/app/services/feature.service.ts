import { Injectable } from '@angular/core'
import { BaseApiEntityService } from './BaseApiEntity.service'
import { FeatureModelDto } from '../shared/FeatureModelDto'
import { HttpClient } from '@angular/common/http'
import { Config } from '../shared/Config'
import { ClassTransformer } from 'class-transformer'

@Injectable({
  providedIn: 'root'
})
export class FeatureService extends BaseApiEntityService<FeatureModelDto> {
  protected classRef = FeatureModelDto


  constructor(http: HttpClient, config: Config, json: ClassTransformer) {
    super(http, config, json, 'feature')
  }
}
