import { Component, OnInit } from '@angular/core'
import { InputGeneratorDto } from '../../../shared/code/InputGeneratorDto'
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap'

@Component({
  selector:    'app-generator-runner-modal',
  templateUrl: './generator-runner-modal.component.html',
  styleUrls:   ['./generator-runner-modal.component.scss']
})
export class GeneratorRunnerModalComponent implements OnInit {
  generator: InputGeneratorDto
  result: string

  constructor() { }

  ngOnInit() {
    console.log('Generator runner modal')
    console.log(this.generator)
  }

  canCloseSuccess = () => this.result != null
  success = (modal: NgbActiveModal) => modal.close(this.result)

}
