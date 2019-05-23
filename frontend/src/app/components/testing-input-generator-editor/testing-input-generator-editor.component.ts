import { Component, OnInit } from '@angular/core'
import { TestingInputGeneratorService } from '../../services/testingInputGeneratorService'
import { ActivatedRoute, Router } from '@angular/router'
import { retryWhen, switchMap, tap } from 'rxjs/operators'
import { TestingInputGeneratorDto } from '../../shared/code/TestingInputGeneratorDto'
import { of, Subject } from 'rxjs'
import { CodeLanguage } from '../../shared/CodeLanguage'
import { CodeService } from '../../services/code.service'

@Component({
  selector:    'app-input-generator-editor',
  templateUrl: './testing-input-generator-editor.component.html',
  styleUrls:   ['./testing-input-generator-editor.component.less']
})
export class TestingInputGeneratorEditorComponent implements OnInit {
  private generator: TestingInputGeneratorDto
  private languageChanged$ = new Subject<CodeLanguage>()
  private add$ = new Subject()

  constructor(private testingInputGeneratorService: TestingInputGeneratorService,
              private activatedRoute: ActivatedRoute,
              private router: Router,
              private codeService: CodeService) { }

  ngOnInit() {
    this.activatedRoute.params.pipe
        (
          switchMap(params => {
            if ('id' in params) {
              return this.testingInputGeneratorService.getById(+params['id'])
            } else {
              return of(TestingInputGeneratorDto.EMPTY())
            }
          }),
          tap(generator => this.generator = generator)
        )
        .subscribe()

    this.languageChanged$.pipe(
      switchMap(lang => this.codeService.scaffoldStartingSnippet(lang)),
      tap(res => this.generator.codeSnippet.code = res.code)
    ).subscribe()


    this.add$.pipe(
      switchMap(() => this.testingInputGeneratorService.save(this.generator)),
      tap(id => this.router.navigate(['generator', id])),
      retryWhen(errors => errors.pipe(
        tap(e => console.error(e))
      )),
    ).subscribe()
  }
}
