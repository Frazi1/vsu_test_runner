import { Component, OnInit } from '@angular/core'
import { AbstractControl, FormBuilder, FormGroup, Validators } from '@angular/forms'
import { AuthService } from '../../services/auth.service'
import { catchError, map, tap } from 'rxjs/operators'
import { AsyncValidatorDebouncedValidator } from '../../asyncValidatorDebouncedValidator'
import { SignUpRequestDto } from '../../shared/SignUpRequestDto'
import { throwError } from 'rxjs'
import { AuthenticationRequestDto } from '../../shared/AuthenticationRequestDto'
import { AuthStorageService } from '../../services/auth-storage.service'
import { ActivatedRoute, Router } from '@angular/router'

@Component({
  selector:    'app-auth',
  templateUrl: './auth.component.html',
  styleUrls:   ['./auth.component.scss']
})
export class AuthComponent implements OnInit {

  // username: string
  // password: string

  isSignUp = true

  form: FormGroup

  constructor(private fb: FormBuilder,
              private authService: AuthService,
              private authStorageService: AuthStorageService,
              private activatedRoute: ActivatedRoute,
              private router: Router) { }

  ngOnInit() {
    this.isSignUp = this.activatedRoute.snapshot.data['isSignUp']
    let usernameAsyncValidators = this.isSignUp === true ? [
        new AsyncValidatorDebouncedValidator(val => this.authService.isUsernameTaken(val).pipe(
          map(res => res === true ? {usernameTaken: true} : null)
        )).validate
      ]
      : []
    let controlsConfig = {
      username: [
        '',
        [Validators.required],
        usernameAsyncValidators
      ],
      password: [
        '',
        [Validators.required]
      ]
    }
    this.form = this.fb.group(controlsConfig)
  }

  public get username(): AbstractControl {
    return this.form.get('username')
  }

  public get password(): AbstractControl {
    return this.form.get('password')
  }

  public submit() {
    if (this.isSignUp) {
      this.signUp()
    } else {
      this.signIn()
    }
  }

  private signUp() {
    this.authService.signUp(new SignUpRequestDto(this.username.value, this.password.value)).pipe(
      catchError(err => {
        console.error(err)
        return throwError(err)
      }),
      tap(() => console.log('Success registration'))
    ).subscribe()
  }

  private signIn() {
    let usernameValue = this.username.value
    let passwordValue = this.password.value
    this.authService.authenticate(new AuthenticationRequestDto(usernameValue, passwordValue)).pipe(
      tap(res => this.authStorageService.setAccessToken(res.accessToken)),
      tap (() => this.authStorageService.setUsername(usernameValue)),
      tap(() => this.router.navigate(['']))
    ).subscribe()
  }

  public signUpClick() {
    this.router.navigate(['/auth', 'signup'])
  }
}

