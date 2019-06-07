import { Component, OnInit } from '@angular/core'
import { GeneratorService } from '../../../services/generator.service'
import { ActivatedRoute, Router } from '@angular/router'
import { retryWhen, switchMap, tap } from 'rxjs/operators'
import { InputGeneratorDto } from '../../../shared/code/InputGeneratorDto'
import { of, Subject } from 'rxjs'
import { CodeLanguage } from '../../../shared/CodeLanguage'
import { CodeService } from '../../../services/code.service'
import { BaseComponent } from '../../base.component'

@Component({
  selector:    'app-input-generator-editor',
  templateUrl: './generator-editor.component.html',
  styleUrls:   ['./generator-editor.component.scss']
})
export class GeneratorEditorComponent extends BaseComponent implements OnInit {
  private generator: InputGeneratorDto
  private languageChanged$ = new Subject<CodeLanguage>()
  private add$ = new Subject()
  update$ = new Subject()

  constructor(private testingInputGeneratorService: GeneratorService,
              private activatedRoute: ActivatedRoute,
              private router: Router,
              private codeService: CodeService) {
    super()
  }

  ngOnInit() {
    this.paramsSub()
    this.languagesSub()
    this.addSub()
    this.updateSub()
  }

  public get isCreatingNew(): boolean {
    return this.generator == null || this.generator.id == null
  }

  private languagesSub() {
    this.languageChanged$.pipe(
      switchMap(lang => this.codeService.scaffoldStartingSnippet(lang)),
      tap(res => this.generator.codeSnippet.code = res.code)
    ).subscribe()
  }

  private paramsSub() {
    this.activatedRoute.params.pipe
        (
          switchMap(params => {
            if ('id' in params) {
              return this.testingInputGeneratorService.getById(+params['id'])
            } else {
              return of(InputGeneratorDto.EMPTY())
            }
          }),
          tap(generator => this.generator = generator)
        )
        .subscribe()
  }

  private addSub() {
    this.add$.pipe(
      switchMap(() => this.testingInputGeneratorService.save(this.generator)),
      tap(id => this.router.navigate(['generator', id])),
      retryWhen(errors => errors.pipe(
        tap(e => console.error(e))
      )),
    ).subscribe()
  }

  private updateSub() {
    this.createGuardedObservable(this.update$).pipe(
      tap(() => console.log('Update clicked')),
      switchMap(() => this.testingInputGeneratorService.update(this.generator)),
      switchMap(() => this.testingInputGeneratorService.getById(this.generator.id)),
      retryWhen(errors => errors.pipe(
        tap(e => console.error(e))
      )),
      tap(gen => this.generator = gen)
    ).subscribe()
  }
}
