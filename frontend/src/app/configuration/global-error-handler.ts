import { ErrorHandler, Injectable } from '@angular/core'
import { ToastrService } from 'ngx-toastr'
import { HttpErrorResponse } from '@angular/common/http'

@Injectable({
  providedIn: 'root'
})
export class GlobalErrorHandler implements ErrorHandler {
  constructor(private toastr: ToastrService) {
  }

  handleError(error: any): void {
    if (error instanceof HttpErrorResponse) {
      // noinspection TypeScriptValidateTypes
      this.toastr.error(error.error.message || error.message, 'Server error',
        {onActivateTick: true}
      )
    } else {
      setTimeout(() => this.toastr.error(error.message, 'Unexpected error', {onActivateTick: true}))
    }
    console.error(error)
  }
}
