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

  get cumulatedPlotSrc() {
    return this.getPlotSrc('cumulated');
  }

  get dailyPlotSrc() {
    return this.getPlotSrc('daily');
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
      // let ss = polygonTemplate.states.create('active');
      // ss.properties.fill = chart.colors.getIndex(2);

      let hs = polygonTemplate.states.create('hover');
      hs.properties.fill = chart.colors.getIndex(4);

      //Set min/max fill color for each area
      polygonSeries.heatRules.push({
        property: 'fill',
        target: polygonSeries.mapPolygons.template,
        min: chart.colors.getIndex(1).brighten(1),
        max: chart.colors.getIndex(1).brighten(-0.3),
      });

      polygonSeries.data = [
        { id: 'baden-württemberg', value: 5450.0 },
        { id: 'bavaria', value: 6940.0 },
        { id: 'berlin', value: 1205.0 },
        { id: 'brandenburg', value: 695.0 },
        { id: 'bremen', value: 185.0 },
        { id: 'hamburg', value: 467.0 },
        { id: 'hesse', value: 1875.0 },
        { id: 'mecklenburg-western_pomerania', value: 145.0 },
        { id: 'lower_saxony', value: 1938.0 },
        { id: 'north_rhine-westphalia', value: 6049.0 },
        { id: 'rhineland-palatinate', value: 1210.0 },
        { id: 'saarland', value: 425.0 },
        { id: 'saxony', value: 946.0 },
        { id: 'sachsen-anhalt', value: 331.0 },
        { id: 'schleswig-holstein', value: 566.0 },
        { id: 'thuringia', value: 591.0 },
      ].map((x) => {
        x.id = (self.chart.geodata as any).features.find(
          (f) => self.cleanLandName(f.properties.name) == x.id
        ).id;
        return x;
      });
      // Set up heat legend
      let heatLegend = chart.createChild(am4maps.HeatLegend);
      heatLegend.series = polygonSeries;
      heatLegend.align = 'right';
      heatLegend.valign = 'bottom';
      heatLegend.width = am4core.percent(20);
      heatLegend.marginRight = am4core.percent(4);
      heatLegend.minValue = 0;
      heatLegend.maxValue = 7000;

      // Set up custom heat map legend labels using axis ranges
      let minRange = heatLegend.valueAxis.axisRanges.create();
      minRange.value = heatLegend.minValue;
      let maxRange = heatLegend.valueAxis.axisRanges.create();
      maxRange.value = heatLegend.maxValue;
      maxRange.label.text = heatLegend.maxValue.toString();
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

  private getPlotSrc(suffix: string) {
    return this.selectedLand
      ? this.sanitizer.bypassSecurityTrustResourceUrl(
          `assets/map_${this.selectedLand}_${suffix}.html`
        )
      : null;
  }
}
