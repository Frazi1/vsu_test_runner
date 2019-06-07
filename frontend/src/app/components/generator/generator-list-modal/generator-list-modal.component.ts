import { Component, OnInit } from '@angular/core'
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap'
import { InputGeneratorDto } from '../../../shared/code/InputGeneratorDto'

@Component({
  selector:    'app-generator-list-modal',
  templateUrl: './generator-list-modal.component.html',
  styleUrls:   ['./generator-list-modal.component.scss']
})
export class GeneratorListModalComponent implements OnInit {
  public selectedItem: InputGeneratorDto

  constructor() {
  }

  ngOnInit() {
  }

  success = (modal: NgbActiveModal) => modal.close(this.selectedItem)
  canCloseWithSuccess = () => this.selectedItem != null
}
