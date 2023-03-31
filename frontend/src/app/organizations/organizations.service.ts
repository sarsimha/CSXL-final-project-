import { Injectable } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import { AuthenticationService } from '../authentication.service';
import { mergeMap, Observable, of, shareReplay } from 'rxjs';


export interface Organization {
  id?: number;
  name: string;
  description: string;

}
@Injectable({
  providedIn: 'root'
})
export class OrganizationsService {
  public organization$: Observable<Organization[] | undefined>;

  constructor(protected http: HttpClient,  protected auth: AuthenticationService) {
    this.organization$ = this.auth.isAuthenticated$.pipe(
      mergeMap(isAuthenticated => {
        if (isAuthenticated) {
          return this.getAllOrganizations()
        } else {
          return of(undefined);
        }
      }),
      shareReplay(1)
    );
  }


  getAllOrganizations(): Observable<Organization[]>{
    return this.http.get<Organization[]>('/api/organization')
  }

}
