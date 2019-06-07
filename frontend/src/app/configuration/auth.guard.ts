import { Injectable } from '@angular/core'
import {
  CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router, CanActivateChild, UrlTree
} from '@angular/router'
import { Observable } from 'rxjs'
import { AuthStorageService } from '../services/auth-storage.service'

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate, CanActivateChild {

  constructor(private authStorage: AuthStorageService,
              private router: Router) {

  }

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean> | Promise<boolean> | boolean {

    return this.canActiavateInternal()
  }

  public canActivateChild(childRoute: ActivatedRouteSnapshot,
                          state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
    return this.canActiavateInternal()
  }

  private canActiavateInternal() {
    if (this.authStorage.isAuthenticated) {
      return true
    }
    this.router.navigate(['/auth'])
  }
}
