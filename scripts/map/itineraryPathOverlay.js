import {
   buildItineraryPathD,
   buildRouteMapPoints,
} from './itineraryPathGeometry.js';
import {
   ENTRANCE_LANDMARK,
   ENTRANCE_WALK_NODE_ID,
   ZOO_MAP_HEIGHT_PX,
   ZOO_MAP_WIDTH_PX,
} from '../shared/zooMapConstants.js';

const SVG_NS = 'http://www.w3.org/2000/svg';
const ITINERARY_PATH_LAYER_ID = 'itinerary-path';
const PATH_CLASS = 'itinerary-path-line';

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

function withEntranceLandmark(points = []) {
   if (points.length === 0 || points[0].nodeId !== ENTRANCE_WALK_NODE_ID) {
      return points;
   }

   return [ENTRANCE_LANDMARK, ...points];
}

function buildPathD(points = []) {
   const routePoints = buildRouteMapPoints(points, {
      withEntranceLandmark,
      pointToMapPx,
   });

   return buildItineraryPathD(routePoints);
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
