import { Component, OnInit } from '@angular/core';
import { interval } from 'rxjs';
import { WrocsidService } from 'src/app/services/wrocsid/wrocsid.service';
import { environment } from 'src/environments/environment';
import { PlotlyModule } from 'angular-plotly.js';

@Component({
  selector: 'app-targets-location-graph',
  templateUrl: './targets-location-graph.component.html',
  styleUrls: ['./targets-location-graph.component.css']
})
export class TargetsLocationGraphComponent implements OnInit {

  public targets$!:any
  graph!:any

  constructor(private wrocsid: WrocsidService) { }

  ngOnInit(): void {
    this.wrocsid.get_targets_data().subscribe(data => {
      this.targets$ = data
      this.setTargetsLocationGraph()
    })

    interval(60 * 1000).subscribe(() => {
      this.wrocsid.get_targets_data().subscribe(data => {
        if (data) {
            this.targets$ = data
            this.setTargetsLocationGraph()
        }
      })
    })
  }

  setTargetsLocationGraph() {
    if (Array.isArray(this.targets$)) {
      let targets_text = this.targets$.map(target => target.identifier + " | " + target.metadata.ip + " - " + target.metadata.country_code)
      let targets_lat = this.targets$.map(target => target.metadata.lat)
      let targets_lon = this.targets$.map(target => target.metadata.lon)

      let data = [{
        type:'scattermapbox',
        lat: targets_lat,
        lon: targets_lon,
        mode:'markers',
        marker: {
          size:14
        },
        text: targets_text
      }]
      
      let layout = {
        autosize: false,
        hovermode:'closest',
        mapbox: {
          bearing:0,
          center: {
            lat:32,
            lon:35
          },
          pitch:0,
          zoom:7,
        },
        width: 500,
        height: 250,
        margin: {
          l: 120,
          r: 0,
          t: 0,
          b:20
        }
      }

      this.graph = {
        'data': data,
        'layout': layout
      }
      
      PlotlyModule.plotlyjs.setPlotConfig({
        mapboxAccessToken: environment.MABPOX_TOKEN
      })
      
      PlotlyModule.plotlyjs.newPlot('targetsLocationGraph', data, layout)
    }
  }
}
