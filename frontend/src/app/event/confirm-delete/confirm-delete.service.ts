import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { MatDialogRef, MatDialog } from '@angular/material/dialog';
import { ConfirmDeleteComponent } from './confirm-delete.component';

@Injectable({
  providedIn: 'root'
})
export class ConfirmDeleteService {

  private dialogRef!: MatDialogRef<ConfirmDeleteComponent>;

  constructor(private dialog: MatDialog) { }

  public confirm(title: string, message: string): Observable<any> {

    this.dialogRef = this.dialog.open(ConfirmDeleteComponent);
    this.dialogRef.componentInstance.title = title;
    this.dialogRef.componentInstance.message = message;

    return this.dialogRef.afterClosed();
  }

}
