import { Component, OnInit } from '@angular/core'

@Component({
  selector:    'app-nav-menu',
  templateUrl: './nav-menu.component.html',
  styleUrls:   ['./nav-menu.component.less']
})

export class NavMenuComponent implements OnInit {
  items = [
    {name: 'Главная', path: '/'},
    {name: 'Шаблоны', path: '/template'},
    {name: 'Открытые тесты', path: '/instance'},
    {name: 'Мои активные тесты', path: '/run'}
  ]

  constructor() {
    for (const item in this.items) {
      console.log(`key: ${item}, value: ${this.items[item]}`)
    }
  }

  ngOnInit() {
  }
}
