import { Component, OnInit } from '@angular/core'
import { AuthStorageService } from '../../services/auth-storage.service'
import { Router } from '@angular/router'

@Component({
  selector:    'app-logout',
  templateUrl: './logout.component.html',
  styleUrls:   ['./logout.component.scss']
})
export class LogoutComponent implements OnInit {

  constructor(private authStorage: AuthStorageService,
              private router: Router) { }

  ngOnInit() {
    this.authStorage.logout()
    this.router.navigate([''])
  }

}
