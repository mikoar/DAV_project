import { Component, NgZone, AfterViewInit, OnDestroy } from '@angular/core';
import * as am4core from '@amcharts/amcharts4/core';
import * as am4maps from '@amcharts/amcharts4/maps';
import am4geodata_germanyHigh from '@amcharts/amcharts4-geodata/germanyHigh';
import am4themes_animated from '@amcharts/amcharts4/themes/animated';

@Component({
  selector: 'app-interactive-map',
  templateUrl: './interactive-map.component.html',
  styleUrls: ['./interactive-map.component.scss'],
})
export class InteractiveMapComponent implements AfterViewInit, OnDestroy {
  private chart: am4maps.MapChart;

  constructor(private zone: NgZone) {}

  ngAfterViewInit() {
    this.zone.runOutsideAngular(() => {
      am4core.useTheme(am4themes_animated);
      let title = '';

      // Create map instance
      this.chart = am4core.create('map-chart', am4maps.MapChart);
      let chart = this.chart;

      chart.titles.create().text = title;

      // Set map definition
      chart.geodata = am4geodata_germanyHigh;

      // Set projection
      chart.projection = new am4maps.projections.Mercator();

      // Create map polygon series
      let polygonSeries = chart.series.push(new am4maps.MapPolygonSeries());

      // Make map load polygon data (state shapes and names) from GeoJSON
      polygonSeries.useGeodata = true;

      // Configure series tooltip
      let polygonTemplate = polygonSeries.mapPolygons.template;
      polygonTemplate.tooltipText = '{name}: {value}';
      polygonTemplate.nonScalingStroke = true;
      polygonTemplate.strokeWidth = 0.5;

      // Create hover state and set alternative fill color
      let hs = polygonTemplate.states.create('hover');
      hs.properties.fill = chart.colors.getIndex(1).brighten(-0.5);
    });
  }

  ngOnDestroy() {
    this.zone.runOutsideAngular(() => {
      if (this.chart) {
        this.chart.dispose();
      }
    });
  }
}
