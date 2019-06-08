import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { BaseComponent } from '../../base.component'
import { InputGeneratorDto } from '../../../shared/code/InputGeneratorDto'
import { ActivatedRoute, Router } from '@angular/router'
import { map, switchMap, takeUntil, tap } from 'rxjs/operators'
import { GeneratorService } from '../../../services/generator.service'
import { of, race } from 'rxjs'

@Component({
  selector:    'app-generator-list',
  templateUrl: './generator-list.component.html',
  styleUrls:   ['./generator-list.component.scss']
})
export class GeneratorListComponent extends BaseComponent implements OnInit {
  generators: InputGeneratorDto[]

  @Input()
  allowSelection: boolean = false

  @Input()
  selectedItem: InputGeneratorDto = null

  @Output()
  selectedItemChange = new EventEmitter<InputGeneratorDto>()

  constructor(private activatedRoute: ActivatedRoute,
              private generatorService: GeneratorService,
              private router: Router) {
    super()
  }

  public onClick(item: InputGeneratorDto): void {
    if (this.allowSelection === true) {
      this.setSelection(item)
    } else {
      this.navigateToSelection(item)
    }
  }

  private setSelection(item: InputGeneratorDto): void {
    this.selectedItem = item
    this.selectedItemChange.emit(item)
  }

  private navigateToSelection(item: InputGeneratorDto): void {
    this.router.navigate(['generator', item.id])
  }

  ngOnInit() {
    race(
      this.activatedRoute.data.pipe(
        map(data => data.list as InputGeneratorDto[]),
        switchMap(gens => gens == null ? of() : of(gens))
      ),
      this.generatorService.getAll()
    ).pipe(
      takeUntil(this.onDestroy$),
      tap(res => this.generators = res)
    ).subscribe()
  }
}
