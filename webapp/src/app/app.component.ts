import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatTableDataSource } from '@angular/material/table';
import { EditFormComponent } from './edit-form/edit-form.component';

export interface PersonRecord {
  pid: number;
  name: string;
  age: number;
  phone: string;
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'webapp';
  displayedColumns: string[] = ['pid', 'name', 'age', 'phone', 'edit'];
  dataSource = new MatTableDataSource<PersonRecord>();

  constructor(public dialog: MatDialog, private snackBar: MatSnackBar) {
    fetch('/api/fetch').then(response => response.json()).then(data => {
      this.dataSource.data = data.data;
    });
  }

  notify(message: string): void {
    this.snackBar.open(message, 'Close', {
      duration: 3000
    });
  }

  submit(records: PersonRecord[], callback: (success: boolean) => void): void {
    const data = new FormData();
    data.append('data', JSON.stringify({ data: records }));
    fetch('/api/upload', {
      method: 'POST',
      body: data
    }
    ).then((response) => {
      if (response.ok) {
        this.notify('Your change has been saved');
      } else {
        this.notify(response.statusText);
      }
      callback(response.ok);
    }).catch(err => {
      this.notify(err);
      callback(false);
    });
  }

  removeRecord(pid: number): void {
    const tmp: PersonRecord[] = [];
    this.dataSource.data.forEach(element => {
      if (element.pid !== pid) {
        tmp.push({ ...element });
      }
    });

    this.submit(tmp, success => {
      if (success) {
        this.dataSource.data = tmp;
      }
    });
  }

  lookupRecord(pid: number): number {
    let retIdx = -1;
    this.dataSource.data.forEach((element, idx) => {
      if (element.pid === pid) {
        retIdx = idx;
      }
    });
    return retIdx;
  }

  addOrUpdateRecord(person: PersonRecord): void {
    const idx = this.lookupRecord(person.pid);
    const newData = this.dataSource.data;
    if (idx !== -1) {
      newData[idx] = { ...person };
    } else {
      newData.push(person);
    }
    this.submit(newData, success => {
      if (success) {
        this.dataSource.data = newData;
      }
    });
  }

  openDialog(prepopulated: PersonRecord | null, callback: (record: PersonRecord | null) => void): void {
    const dialogRef = this.dialog.open(EditFormComponent, {
      data: prepopulated
    });

    dialogRef.afterClosed().subscribe({
      next: result => {
        if (result) {
          callback(result);
        } else {
          callback(null);
        }
      }
    });
  }

  createNewRecord(): void {
    this.openDialog(null, (record: PersonRecord | null) => {
      if (record !== null) {
        this.addOrUpdateRecord(record);
      }
    });
  }

  editRecord(pid: number): void {
    const idx = this.lookupRecord(pid);
    this.openDialog({ ...this.dataSource.data[idx] }, (record: PersonRecord | null) => {
      if (record !== null) {
        this.addOrUpdateRecord(record);
      }
    });
  }
}
