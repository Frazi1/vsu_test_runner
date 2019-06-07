import { Component, Input, OnInit } from '@angular/core'
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap'

@Component({
  selector:    'app-modal-ok-cancel',
  templateUrl: './modal-ok-cancel.component.html',
  styleUrls:   ['./modal-ok-cancel.component.scss']
})
export class ModalOkCancelComponent implements OnInit {

  @Input()
  canCloseSuccess: (modal: NgbActiveModal) => boolean

  @Input()
  success: (modal: NgbActiveModal) => void

  constructor(private activeModal: NgbActiveModal) { }

  ngOnInit() {
  }

  public cancel() {
    this.activeModal.dismiss('Cancel')
  }

  public successInternal() {
    if (this.success) {
      this.success(this.activeModal)
    } else {
      this.activeModal.close()
    }
  }

  public canCloseSuccessInternal() {
    if (this.canCloseSuccess) {
      return this.canCloseSuccess(this.activeModal)
    }
    return true
  }
}
