import { ItineraryPathCalculator } from './itineraryPathCalculator.js';
import { ItineraryPathConstants } from './itineraryPathConstants.js';
import { ItineraryPathRenderer } from './itineraryPathRenderer.js';
import { SvgConstants } from '../shared/svgConstants.js';
import { ZooMapConstants } from '../shared/zooMapConstants.js';

export class ItineraryPathOverlayRenderer {
   static SVG_NS = SvgConstants.SVG_NS;

   static ITINERARY_PATH_LAYER_ID = 'itinerary-path';

   static PATH_CLASS = 'itinerary-path-line';

   static ARROWS_CLASS = 'itinerary-path-arrows';

   static ARROW_CLASS = 'itinerary-path-arrow';

   static ARROW_HEAD_POINTS = '0,-2.5 12,0 0,2.5';

   static getSvgRoot() {
      return document.querySelector('#zooMapMount svg');
   }

   static pointToMapPx(point) {
      if (Number.isFinite(point.xPx) && Number.isFinite(point.yPx)) {
         return {
            x: point.xPx,
            y: point.yPx,
         };
      }

      if (Number.isFinite(point.x) && Number.isFinite(point.y)) {
         return {
            x: point.x / 100 * ZooMapConstants.ZOO_MAP_WIDTH_PX,
            y: point.y / 100 * ZooMapConstants.ZOO_MAP_HEIGHT_PX,
         };
      }

      return null;
   }

   static buildPathD(itineraryPath) {
      if (itineraryPath.legs.length > 0) {
         return ItineraryPathCalculator.buildItineraryPathDFromWalkLegs(
            itineraryPath.legs,
            itineraryPath.points,
            { pointToMapPx: ItineraryPathOverlayRenderer.pointToMapPx }
         );
      }

      const routePoints = ItineraryPathCalculator.buildRouteMapPoints(itineraryPath.points, {
         withEntranceLandmark: (normalizedPoints) => normalizedPoints,
         pointToMapPx: ItineraryPathOverlayRenderer.pointToMapPx,
      });

      return ItineraryPathCalculator.buildItineraryPathD(routePoints);
   }

   static createArrowMarker({ x, y, angleDeg }) {
      const markerGroup = document.createElementNS(ItineraryPathOverlayRenderer.SVG_NS, 'g');
      markerGroup.classList.add(ItineraryPathOverlayRenderer.ARROW_CLASS);
      markerGroup.setAttribute(
         'transform',
         `translate(${x} ${y}) rotate(${angleDeg})`
      );

      const head = document.createElementNS(ItineraryPathOverlayRenderer.SVG_NS, 'polygon');
      head.setAttribute('points', ItineraryPathOverlayRenderer.ARROW_HEAD_POINTS);
      markerGroup.appendChild(head);

      return markerGroup;
   }

   static appendArrowMarkers(markersLayer, pathD) {
      if (!pathD) {
         return;
      }

      for (const placement of ItineraryPathRenderer.buildPathArrowPlacements(pathD)) {
         markersLayer.appendChild(ItineraryPathOverlayRenderer.createArrowMarker(
            ItineraryPathRenderer.offsetArrowPlacement(
               placement,
               ItineraryPathConstants.ITINERARY_PATH_ARROW_SIDE_OFFSET_PX,
               'left'
            )
         ));
      }
   }

   static createPathLayer(pathD) {
      const layer = document.createElementNS(ItineraryPathOverlayRenderer.SVG_NS, 'g');
      layer.setAttribute('id', ItineraryPathOverlayRenderer.ITINERARY_PATH_LAYER_ID);
      layer.setAttribute('aria-hidden', 'true');

      const path = document.createElementNS(ItineraryPathOverlayRenderer.SVG_NS, 'path');
      path.classList.add(ItineraryPathOverlayRenderer.PATH_CLASS);
      path.setAttribute('d', pathD);
      path.setAttribute('fill', 'none');
      layer.appendChild(path);

      const markersLayer = document.createElementNS(ItineraryPathOverlayRenderer.SVG_NS, 'g');
      markersLayer.classList.add(ItineraryPathOverlayRenderer.ARROWS_CLASS);
      ItineraryPathOverlayRenderer.appendArrowMarkers(markersLayer, pathD);
      layer.appendChild(markersLayer);

      return layer;
   }

   static removeItineraryPathLayer(svgRoot) {
      if (!svgRoot) {
         return;
      }

      svgRoot.querySelector(`#${ItineraryPathOverlayRenderer.ITINERARY_PATH_LAYER_ID}`)?.remove();
   }
}
