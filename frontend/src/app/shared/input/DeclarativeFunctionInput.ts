import { DeclarativeInputItem } from './DeclarativeInputItem'
import { Type } from 'class-transformer'

export class DeclarativeFunctionInput {

  id: number = undefined

  @Type(() => DeclarativeInputItem)
  items: DeclarativeInputItem[] = undefined
}
