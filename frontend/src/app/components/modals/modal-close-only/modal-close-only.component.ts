import { Component, OnInit } from '@angular/core'
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap'

@Component({
  selector:    'app-modal-close-only',
  templateUrl: './modal-close-only.component.html',
  styleUrls:   ['./modal-close-only.component.scss']
})
export class ModalCloseOnlyComponent implements OnInit {

  constructor(private activeModal: NgbActiveModal) { }

  ngOnInit() {
  }

  public close() {
    this.activeModal.close()
  }
}
