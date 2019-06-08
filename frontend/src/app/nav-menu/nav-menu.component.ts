import { Component, OnInit } from '@angular/core'

@Component({
  selector:    'app-nav-menu',
  templateUrl: './nav-menu.component.html',
  styleUrls:   ['./nav-menu.component.scss']
})

export class NavMenuComponent implements OnInit {
  items = [
    {name: 'Главная', path: '/'},
    {name: 'Шаблоны', path: '/template'},
    {name: 'Генераторы', path: '/generator'},
    {name: 'Менеджмент', path: '/management'},
    {name: 'Открытые тесты', path: '/instance'},
    {name: 'Мои активные тесты', path: '/run'},
    {name: 'Выйти', path: '/logout'}
  ]

  constructor() {
    for (const item of this.items) {
      console.log(`key: ${item}, value: ${this.items.find(i => i == item)}`)
    }
  }

  ngOnInit() {
  }
}
