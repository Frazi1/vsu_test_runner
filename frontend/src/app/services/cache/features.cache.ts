import { FeatureModelDto } from '../../shared/FeatureModelDto'
import { Observable } from 'rxjs'
import { BaseCacheService } from './base-cache.service'
import { Injectable } from '@angular/core'
import { FeatureService } from '../feature.service'

@Injectable({
  providedIn: 'root'
})
class FeaturesCache extends BaseCacheService<FeatureModelDto[]> {

  constructor(private featureService: FeatureService) {super() }

  protected dataProvider(): () => Observable<FeatureModelDto[]> {
    return () => this.featureService.getAll()
  }
}
