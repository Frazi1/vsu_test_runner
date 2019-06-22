import { Component, OnInit } from '@angular/core'
import { QuestionBankService } from '../../../services/question-bank.service'
import { Observable } from 'rxjs'
import { QuestionBankSectionDto } from '../../../shared/question-bank/QuestionBankSectionDto'
import { BaseComponent } from '../../base.component'

@Component({
  selector:    'app-question-bank-list',
  templateUrl: './question-bank-list.component.html',
  styleUrls:   ['./question-bank-list.component.scss']
})
export class QuestionBankListComponent extends BaseComponent implements OnInit {

  sections$: Observable<QuestionBankSectionDto[]>

  constructor(private questionBankService: QuestionBankService) {
    super()
  }

  ngOnInit() {
    this.sections$ = this.questionBankService.getAll()
  }

}
