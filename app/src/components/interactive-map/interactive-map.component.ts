import { Component, NgZone, AfterViewInit, OnDestroy } from '@angular/core';
import * as am4core from '@amcharts/amcharts4/core';
import * as am4maps from '@amcharts/amcharts4/maps';
import am4geodata_germanyHigh from '@amcharts/amcharts4-geodata/germanyHigh';
import am4themes_animated from '@amcharts/amcharts4/themes/animated';
import { last } from '@amcharts/amcharts4/.internal/core/utils/Array';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-interactive-map',
  templateUrl: './interactive-map.component.html',
  styleUrls: ['./interactive-map.component.scss'],
})
export class InteractiveMapComponent implements AfterViewInit, OnDestroy {
  private chart: am4maps.MapChart;
  private selectedLand: SafeUrl;

  get mapSrc() {
    return this.selectedLand
      ? this.sanitizer.bypassSecurityTrustResourceUrl(
          `assets/map_${this.selectedLand}.html`
        )
      : null;
  }

  constructor(private zone: NgZone, private sanitizer: DomSanitizer) {}

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
      polygonTemplate.tooltipText = '{name}';
      polygonTemplate.togglable = true;
      polygonTemplate.applyOnClones = true;
      polygonTemplate.nonScalingStroke = true;
      polygonTemplate.strokeWidth = 0.5;

      let lastSelected: am4maps.MapPolygon;

      let self = this;
      polygonTemplate.events.on('hit', function (ev) {
        if (lastSelected) {
          // This line serves multiple purposes:
          // 1. Clicking a country twice actually de-activates, the line below
          //    de-activates it in advance, so the toggle then re-activates, making it
          //    appear as if it was never de-activated to begin with.
          // 2. Previously activated countries should be de-activated.
          lastSelected.isActive = false;
        }
        // ev.target.series.chart.zoomToMapObject(ev.target);
        if (lastSelected !== ev.target) {
          lastSelected = ev.target;
          self.zone.run(
            () =>
              (self.selectedLand = self.cleanLandName(
                lastSelected.dataItem.dataContext['name']
              ))
          );
        }
      });

      /* Create selected and hover states and set alternative fill color */
      let ss = polygonTemplate.states.create('active');
      ss.properties.fill = chart.colors.getIndex(2);

      let hs = polygonTemplate.states.create('hover');
      hs.properties.fill = chart.colors.getIndex(4);
    });
  }

  ngOnDestroy() {
    this.zone.runOutsideAngular(() => {
      if (this.chart) {
        this.chart.dispose();
      }
    });
  }

  private cleanLandName(name: string) {
    return name.toLowerCase().replace(' ', '_');
  }
}
