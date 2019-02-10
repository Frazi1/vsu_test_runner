import {ErrorHandler, Injectable} from '@angular/core';
import {ToastrService} from 'ngx-toastr';
import {HttpErrorResponse} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class GlobalErrorHandler implements ErrorHandler {
  constructor(private toastr: ToastrService) {
  }

  handleError(error: any): void {
    if (error instanceof HttpErrorResponse) {
      this.toastr.error(error.error.message, 'Server error', {onActivateTick: true});
    }
    console.error(error.error);
  }
}
