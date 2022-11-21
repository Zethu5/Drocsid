import { Component, OnInit } from '@angular/core';
import { environment  } from '../../../environments/environment'
@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css',]
})
export class NavbarComponent implements OnInit {

  invite_link: string = ""

  constructor() { }

  ngOnInit(): void {
    this.invite_link = 'https://discord.gg/'.concat(environment.INVITE_ID)
  }
}
