import { Component, Input, OnInit } from '@angular/core';
import { PlotlyModule } from 'angular-plotly.js';
import { interval } from 'rxjs';
import { Target } from 'src/app/Model';
import { WrocsidService } from 'src/app/services/wrocsid/wrocsid.service';

@Component({
  selector: 'app-target-health-check',
  templateUrl: './target-health-check.component.html',
  styleUrls: ['./target-health-check.component.css']
})
export class TargetHealthCheckComponent implements OnInit {
  @Input() target$!: Target
  target_pings$!:any
  graph!:any

  constructor(private wrocsid: WrocsidService) { }

  ngOnInit(): void {
    this.wrocsid.getTargetPings(this.target$.identifier).subscribe((data) => {
      this.setTargetStatusGraph(data)
    })

    interval(10 * 1000).subscribe(() => {
      this.wrocsid.getTargetPings(this.target$.identifier).subscribe(data => {
        if (data) {
          this.setTargetStatusGraph(data)
        }
      })
    })
  }

  setTargetStatusGraph(data: any) {
    let x_data = []
    let y_data = []

    if(Array.isArray(data)){
      for(let i = 0; i < data.length - 1; i++) {

        // check what's the diffs between 2 consecutive pings
        let timedate1 = new Date(data[i])
        let timedate2 = new Date(data[i+1])
        let diff = timedate2.getTime() - timedate1.getTime()
        diff = (diff - diff % 1000) / 1000

        // add current x and y point to the data set
        x_data.push(data[i])
        y_data.push(1)
        
        // check if there was a 'drop' in pings,
        // ping is every 60 seconds, giving extra second as a buffer
        // to see if the ping didn't come in 1 minute
        if (diff > 61) {
          // calculate the amount of minutes a ping didn't show up
          diff = (diff - diff % 60) / 60

          // add the x,y data to the set as an indication that a ping didn't show up
          for(let j = 0; j <= diff; j++) {
            y_data.push(0)
            x_data.push(new Date(timedate1.getTime() + j * 60 * 1000))
          }
        }
      }

      // init the graph with the completed set
      this.graph = {
        data: [{
          x: x_data,
          y: y_data,
          mode: "lines"
        }],
        layout: {
          xaxis: {title: "TIMESPAN"},
          yaxis: {title: "STATUS", tickmode: 'array', ticktext: ['ONLINE', 'OFFLINE'], tickvals: [1, 0]},
          title: "TARGET STATUS TIMESPAN",
          width: 450,
          margin: {
            l: 120,
            r: 0
          }
        }
      }
    }
  }
}