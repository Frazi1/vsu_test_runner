import { TestQuestionTemplate } from './TestQuestionTemplate'
import { Type } from 'class-transformer'


export class TestTemplate {

  id: number
  isDeleted: boolean = undefined
  name: string
  timeLimit: number

  @Type(() => TestQuestionTemplate)
  questionTemplates: TestQuestionTemplate[]


  constructor(id: number                                = null,
              name: string                              = '',
              timeLimit: number                         = null,
              questionTemplates: TestQuestionTemplate[] = []) {
    this.id = id
    this.name = name
    this.timeLimit = timeLimit
    this.questionTemplates = questionTemplates
  }
}
