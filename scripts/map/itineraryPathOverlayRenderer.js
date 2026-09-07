import { ItineraryPathArrows } from './itineraryPathArrows.js';
import { ItineraryPathConstants } from './itineraryPathConstants.js';
import { ItineraryPathGeometry } from './itineraryPathGeometry.js';
import { ZooMapConstants } from '../shared/zooMapConstants.js';

const SVG_NS = 'http://www.w3.org/2000/svg';

const ITINERARY_PATH_LAYER_ID = 'itinerary-path';

const PATH_CLASS = 'itinerary-path-line';

const ARROWS_CLASS = 'itinerary-path-arrows';

const ARROW_CLASS = 'itinerary-path-arrow';

const ARROW_HEAD_POINTS = '0,-2.5 12,0 0,2.5';

export class ItineraryPathOverlayRenderer {
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
         return ItineraryPathGeometry.buildItineraryPathDFromWalkLegs(
            itineraryPath.legs,
            itineraryPath.points,
            { pointToMapPx: ItineraryPathOverlayRenderer.pointToMapPx }
         );
      }

      const routePoints = ItineraryPathGeometry.buildRouteMapPoints(itineraryPath.points, {
         withEntranceLandmark: (normalizedPoints) => normalizedPoints,
         pointToMapPx: ItineraryPathOverlayRenderer.pointToMapPx,
      });

      return ItineraryPathGeometry.buildItineraryPathD(routePoints);
   }

   static createArrowMarker({ x, y, angleDeg }) {
      const markerGroup = document.createElementNS(SVG_NS, 'g');
      markerGroup.classList.add(ARROW_CLASS);
      markerGroup.setAttribute(
         'transform',
         `translate(${x} ${y}) rotate(${angleDeg})`
      );

      const head = document.createElementNS(SVG_NS, 'polygon');
      head.setAttribute('points', ARROW_HEAD_POINTS);
      markerGroup.appendChild(head);

      return markerGroup;
   }

   static appendArrowMarkers(markersLayer, pathD) {
      if (!pathD) {
         return;
      }

      for (const placement of ItineraryPathArrows.buildPathArrowPlacements(pathD)) {
         markersLayer.appendChild(ItineraryPathOverlayRenderer.createArrowMarker(
            ItineraryPathArrows.offsetArrowPlacement(
               placement,
               ItineraryPathConstants.ITINERARY_PATH_ARROW_SIDE_OFFSET_PX,
               'left'
            )
         ));
      }
   }

   static createPathLayer(pathD) {
      const layer = document.createElementNS(SVG_NS, 'g');
      layer.setAttribute('id', ITINERARY_PATH_LAYER_ID);
      layer.setAttribute('aria-hidden', 'true');

      const path = document.createElementNS(SVG_NS, 'path');
      path.classList.add(PATH_CLASS);
      path.setAttribute('d', pathD);
      path.setAttribute('fill', 'none');
      layer.appendChild(path);

      const markersLayer = document.createElementNS(SVG_NS, 'g');
      markersLayer.classList.add(ARROWS_CLASS);
      ItineraryPathOverlayRenderer.appendArrowMarkers(markersLayer, pathD);
      layer.appendChild(markersLayer);

      return layer;
   }

   static removeItineraryPathLayer(svgRoot) {
      if (!svgRoot) {
         return;
      }

      svgRoot.querySelector(`#${ITINERARY_PATH_LAYER_ID}`)?.remove();
   }
}
