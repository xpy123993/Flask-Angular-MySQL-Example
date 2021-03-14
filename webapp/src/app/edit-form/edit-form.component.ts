import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { PersonRecord } from '../app.component';

@Component({
  selector: 'app-edit-form',
  templateUrl: './edit-form.component.html',
  styleUrls: ['./edit-form.component.css']
})
export class EditFormComponent implements OnInit {

  record: PersonRecord = {
    pid: 0,
    name: '',
    age: 0,
    phone: ''
  };

  constructor(@Inject(MAT_DIALOG_DATA) public data: PersonRecord|null) { 
    if (data !== null) {
      this.record = data;
    }
  }

  ngOnInit(): void {
  }

}
