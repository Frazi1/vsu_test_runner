import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { BaseComponent } from '../../base.component'
import { QuestionBankService } from '../../../services/question-bank.service'
import { Observable } from 'rxjs'
import { QuestionBankSectionDto } from '../../../shared/question-bank/QuestionBankSectionDto'

@Component({
  selector:    'app-section-selector',
  templateUrl: './section-selector.component.html',
  styleUrls:   ['./section-selector.component.scss']
})
export class SectionSelectorComponent extends BaseComponent implements OnInit {

  nullSection: QuestionBankSectionDto = QuestionBankSectionDto.NullSection()
  sections$: Observable<QuestionBankSectionDto[]>

  @Input()
  value: QuestionBankSectionDto

  @Output()
  valueChange = new EventEmitter<QuestionBankSectionDto>()

  constructor(private questionBankService: QuestionBankService) {
    super()
  }

  ngOnInit() {
    this.sections$ = this.questionBankService.getSectionHeaders()
  }

  onChange(newValue: QuestionBankSectionDto): void {
    this.valueChange.emit(newValue)
  }

}
