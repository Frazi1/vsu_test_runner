import { DeclarativeInputArgumentItem } from './DeclarativeInputArgumentItem'
import { Type } from 'class-transformer'

export class DeclarativeInputItem {

  id: number = undefined

  @Type(() => DeclarativeInputArgumentItem)
  argumentItems: DeclarativeInputArgumentItem[] = undefined

  outputValue: string = undefined

}
