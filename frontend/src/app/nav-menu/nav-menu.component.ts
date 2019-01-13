import {Component, OnInit} from '@angular/core';

@Component({
  selector: 'app-nav-menu',
  templateUrl: './nav-menu.component.html',
  styleUrls: ['./nav-menu.component.less']
})

export class NavMenuComponent implements OnInit {
  private items = [
    {name: 'Главная', path: '/'},
    {name: 'Шаблоны', path: '/template'},
  ];

  constructor() {
    for (const item in this.items) {
      console.log(`key: ${item}, value: ${this.items[item]}`);
    }
  }

  ngOnInit() {
  }
}
