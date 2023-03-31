import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Route } from '@angular/router';
import { isAuthenticated } from 'src/app/gate/gate.guard';



@Component({
  selector: 'app-organizations',
  templateUrl: './organizations.component.html',
  styleUrls: ['./organizations.component.css']
})
export class OrganizationsComponent implements OnInit {
  public static Route: Route = {
    path: 'organizations',
    component: OrganizationsComponent,
    title: 'Organizations', 
    canActivate: [isAuthenticated], 
    // canActivate: [isAuthenticated]
  }

  constructor(route: ActivatedRoute) {

  }

  ngOnInit(): void {
    
  }
}
