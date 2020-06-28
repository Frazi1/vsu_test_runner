import { ErrorHandler, Injectable } from '@angular/core'
import { ToastrService } from 'ngx-toastr'
import { HttpErrorResponse } from '@angular/common/http'

@Injectable({
  providedIn: 'root'
})
export class GlobalErrorHandler implements ErrorHandler {
  constructor(private toastr: ToastrService) {
  }

  getErrorTitle(error: any): string {
    if (error instanceof HttpErrorResponse) return 'Server error'
    return 'Unexpected error'
  }

  handleError(error: any): void {
    alert(error.error || error.message)
    console.error(error)
  }
}
