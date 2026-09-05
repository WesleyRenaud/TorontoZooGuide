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

function getSvgRoot() {
   return document.querySelector('#zooMapMount svg');
}

function pointToMapPx(point) {
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

function buildPathD(itineraryPath) {
   if (itineraryPath.legs.length > 0) {
      return ItineraryPathGeometry.buildItineraryPathDFromWalkLegs(
         itineraryPath.legs,
         itineraryPath.points,
         { pointToMapPx }
      );
   }

   const routePoints = ItineraryPathGeometry.buildRouteMapPoints(itineraryPath.points, {
      withEntranceLandmark: (normalizedPoints) => normalizedPoints,
      pointToMapPx,
   });

   return ItineraryPathGeometry.buildItineraryPathD(routePoints);
}

function createArrowMarker({ x, y, angleDeg }) {
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

function appendArrowMarkers(markersLayer, pathD) {
   if (!pathD) {
      return;
   }

   for (const placement of ItineraryPathArrows.buildPathArrowPlacements(pathD)) {
      markersLayer.appendChild(createArrowMarker(
         ItineraryPathArrows.offsetArrowPlacement(
            placement,
            ItineraryPathConstants.ITINERARY_PATH_ARROW_SIDE_OFFSET_PX,
            'left'
         )
      ));
   }
}

function createPathLayer(pathD) {
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
   appendArrowMarkers(markersLayer, pathD);
   layer.appendChild(markersLayer);

   return layer;
}

function removeItineraryPathLayer(svgRoot) {
   if (!svgRoot) {
      return;
   }

   svgRoot.querySelector(`#${ITINERARY_PATH_LAYER_ID}`)?.remove();
}

export function clearItineraryPathOverlay() {
   removeItineraryPathLayer(getSvgRoot());
}

export function renderItineraryPathOverlay(itineraryPath) {
   const svgRoot = getSvgRoot();

   clearItineraryPathOverlay();

   if (!svgRoot) {
      return;
   }

   const pathD = buildPathD(itineraryPath);

   if (!pathD) {
      return;
   }

   svgRoot.appendChild(createPathLayer(pathD));
}
