import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http'
import { Observable } from 'rxjs/index'
import { Injectable } from '@angular/core'

@Injectable()
export class ContentTypeInterceptor implements HttpInterceptor {
  public intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    let httpRequest = req.clone({
        setHeaders: {'Content-Type': 'application/json; charset=utf-8'}
      }
    )
    return next.handle(httpRequest)
  }

}
