import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http'
import { Observable } from 'rxjs'
import { Injectable } from '@angular/core'
import { AuthStorageService } from '../services/auth-storage.service'

@Injectable()
export class AuthenticationInterceptor implements HttpInterceptor {
  constructor(private authStorage: AuthStorageService) {

  }

  public intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    if (!this.authStorage.isAuthenticated) {
      return next.handle(req)
    }
    const httpRequest = req.clone({
        setHeaders: {'Authorization': `Bearer ${this.authStorage.accessToken}`}
      }
    )
    return next.handle(httpRequest)
  }
}
