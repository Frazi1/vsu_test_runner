import { Observable } from 'rxjs'
import { map } from 'rxjs/operators'
import { BaseService } from './base.service'

export abstract class BaseApiEntityService<T> extends BaseService {

  protected abstract classRef: { new(): T; }

  protected transformOne(value: any): T {
    return this.json.plainToClass(this.classRef, value as Object)
  }

  protected transformMany(value: any[]): T[] {
    return this.json.plainToClass(this.classRef, value as Object[])
  }

  public getById(id: number): Observable<T> {
    return this.http.get(this.buildUrl(id))
               .pipe(
                 map(this.transformOne.bind(this))
               )
  }

  public getAll(): Observable<T[]> {
    return this.http.get(this.buildUrl())
               .pipe(
                 map(this.transformMany.bind(this))
               )
  }
}
