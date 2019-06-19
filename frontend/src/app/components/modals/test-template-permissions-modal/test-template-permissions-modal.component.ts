import { Component, OnInit} from '@angular/core'
import { TestTemplate } from '../../../shared/TestTemplate'

@Component({
  selector:    'app-test-template-permissions-modal',
  templateUrl: './test-template-permissions-modal.component.html',
  styleUrls:   ['./test-template-permissions-modal.component.scss']
})
export class TestTemplatePermissionsModalComponent implements OnInit {

  testTemplate: TestTemplate

  constructor() { }

  ngOnInit() {
  }

}
