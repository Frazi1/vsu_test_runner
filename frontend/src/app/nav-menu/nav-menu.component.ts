import { Component, OnInit } from '@angular/core'
import { AuthStorageService } from '../services/auth-storage.service'

@Component({
  selector:    'app-nav-menu',
  templateUrl: './nav-menu.component.html',
  styleUrls:   ['./nav-menu.component.scss']
})

export class NavMenuComponent implements OnInit {
  items = [
    // {name: 'Главная', path: '/'},
    {name: 'Шаблоны', path: '/template'},
    {name: 'Генераторы', path: '/generator'},
    {name: 'Менеджмент', path: '/management'},
    {name: 'Банк вопросов', path: '/questionBank'},
    {name: 'События', path: '/instance'},
    {name: 'Мои тесты', path: '/run'},
    // {name: 'Выйти', path: '/logout'}
  ]

  itemsRight = [
    {name: 'Выйти', path: '/logout'}
  ]

  constructor(private authStorage: AuthStorageService) {
    for (const item of this.items) {
      console.log(`key: ${item}, value: ${this.items.find(i => i == item)}`)
    }
  }

  ngOnInit() {
  }

  public get currentUserName(): string {
    return this.authStorage.getUsername()
  }
}
