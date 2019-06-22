import { TestQuestionTemplate } from '../TestQuestionTemplate'

export class QuestionBankSectionDto {
  id: number
  name: string

  parentSectionId: number
  parentSection: QuestionBankSectionDto | null
  questionTemplates: TestQuestionTemplate[]

  public static NullSection(): QuestionBankSectionDto {
    let res = new QuestionBankSectionDto()
    res.name = 'Без секции'
    res.id = null
    return res
  }
}
