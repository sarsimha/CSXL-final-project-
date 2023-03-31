import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Route } from '@angular/router';
import { Observable } from 'rxjs';
import { isAuthenticated } from 'src/app/gate/gate.guard';
import { Organization, OrganizationsService } from './organizations.service';



@Component({
  selector: 'app-organizations',
  templateUrl: './organizations.component.html',
  styleUrls: ['./organizations.component.css']
})
export class OrganizationsComponent {
  public static Route: Route = {
    path: 'organizations',
    component: OrganizationsComponent,
    title: 'Organizations', 
    canActivate: [isAuthenticated], 
  }
  public allOrganizations$: Observable<Organization[]>

  constructor(route: ActivatedRoute, private organizationsService: OrganizationsService) {
    this.allOrganizations$ = organizationsService.getAllOrganizations()

  }
}
