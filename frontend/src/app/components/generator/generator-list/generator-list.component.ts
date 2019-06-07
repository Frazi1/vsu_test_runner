import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { BaseComponent } from '../../base.component'
import { InputGeneratorDto } from '../../../shared/code/InputGeneratorDto'
import { ActivatedRoute } from '@angular/router'
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
  selectedItem: InputGeneratorDto = null

  @Output()
  selectedItemChange = new EventEmitter<InputGeneratorDto>()

  constructor(private activatedRoute: ActivatedRoute,
              private generatorService: GeneratorService) {
    super()
  }

  public setSelection(item: InputGeneratorDto): void {
    this.selectedItem = item
    this.selectedItemChange.emit(item)
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
