import { ITINERARY_PATH_ARROW_SIDE_OFFSET_PX } from './itineraryPathConstants.js';
import {
   buildItineraryPathD,
   buildPathArrowPlacements,
   buildRouteMapPoints,
   offsetArrowPlacement,
} from './itineraryPathGeometry.js';
import {
   ZOO_MAP_HEIGHT_PX,
   ZOO_MAP_WIDTH_PX,
} from '../shared/zooMapConstants.js';

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
         x: point.x / 100 * ZOO_MAP_WIDTH_PX,
         y: point.y / 100 * ZOO_MAP_HEIGHT_PX,
      };
   }

   return null;
}

function buildPathD(points = []) {
   const routePoints = buildRouteMapPoints(points, {
      withEntranceLandmark: (normalizedPoints) => normalizedPoints,
      pointToMapPx,
   });

   return buildItineraryPathD(routePoints);
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

   for (const placement of buildPathArrowPlacements(pathD)) {
      markersLayer.appendChild(createArrowMarker(
         offsetArrowPlacement(placement, ITINERARY_PATH_ARROW_SIDE_OFFSET_PX, 'left')
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

   const pathD = buildPathD(itineraryPath?.points);

   if (!pathD) {
      return;
   }

   svgRoot.appendChild(createPathLayer(pathD));
}
