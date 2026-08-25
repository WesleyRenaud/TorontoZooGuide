const SVG_NS = 'http://www.w3.org/2000/svg';
const ROUTE_ARROWS_LAYER_ID = 'transportation-route-arrows';
const ARROWS_CLASS = 'transportation-route-arrows';
const ARROW_CLASS = 'transportation-route-arrow';
const ARROW_HEAD_POINTS = '0,-4.5 20,0 0,4.5';

function getSvgRoot() {
   return document.querySelector('#zooMapMount svg');
}

function setLayerVisibility(svgRoot, layerId, isVisible) {
   svgRoot?.querySelector(layerId)?.style.setProperty(
      'display',
      isVisible ? '' : 'none'
   );
}

function clearRouteMarkerFilters(svgRoot) {
   svgRoot?.querySelectorAll(
      '#zoomobile-route-summer circle[id], #zoomobile-route-winter circle[id]'
   ).forEach((circle) => {
      circle.style.removeProperty('display');
   });
}

function removeRouteArrowsLayer(svgRoot) {
   svgRoot?.querySelector(`#${ROUTE_ARROWS_LAYER_ID}`)?.remove();
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

function circlePoint(circle) {
   const x = Number(circle?.getAttribute?.('cx'));
   const y = Number(circle?.getAttribute?.('cy'));

   if (!Number.isFinite(x) || !Number.isFinite(y)) {
      return null;
   }

   return { x, y };
}

function buildMarkerArrowPlacements(points) {
   const placements = [];

   for (let index = 0; index < points.length - 1; index += 2) {
      const start = points[index];
      const end = points[index + 1];
      const deltaX = end.x - start.x;
      const deltaY = end.y - start.y;

      if (deltaX === 0 && deltaY === 0) {
         continue;
      }

      placements.push({
         x: start.x,
         y: start.y,
         angleDeg: Math.atan2(deltaY, deltaX) * (180 / Math.PI),
      });
   }

   return placements;
}

function appendRouteArrows(svgRoot, routeGroup, markerSequences) {
   removeRouteArrowsLayer(svgRoot);

   if (!svgRoot || !routeGroup) {
      return;
   }

   const arrowsLayer = document.createElementNS(SVG_NS, 'g');
   arrowsLayer.setAttribute('id', ROUTE_ARROWS_LAYER_ID);
   arrowsLayer.setAttribute('aria-hidden', 'true');
   arrowsLayer.classList.add(ARROWS_CLASS);

   const circlesById = new Map(
      Array.from(routeGroup.querySelectorAll('circle[id]')).map((circle) => [
         circle.id,
         circle,
      ])
   );

   for (const markerIds of markerSequences) {
      const points = markerIds
         .map((markerId) => circlePoint(circlesById.get(markerId)))
         .filter(Boolean);

      for (const placement of buildMarkerArrowPlacements(points)) {
         arrowsLayer.appendChild(createArrowMarker(placement));
      }
   }

   if (arrowsLayer.childNodes.length > 0) {
      svgRoot.appendChild(arrowsLayer);
   }
}

export function hideTransportationRouteLayers() {
   const svgRoot = getSvgRoot();

   clearRouteMarkerFilters(svgRoot);
   removeRouteArrowsLayer(svgRoot);
   setLayerVisibility(svgRoot, '#zoomobile-route-summer', false);
   setLayerVisibility(svgRoot, '#zoomobile-route-winter', false);
}

export function showTransportationRouteLayer(route) {
   const svgRoot = getSvgRoot();

   hideTransportationRouteLayers();

   if (!route) {
      return;
   }

   setLayerVisibility(svgRoot, `#zoomobile-route-${route}`, true);
}

export function showTransportationRouteMarkers(route, markerSequences) {
   const svgRoot = getSvgRoot();

   hideTransportationRouteLayers();

   const markerIds = markerSequences.flat();

   if (!route || markerIds.length === 0) {
      return;
   }

   const groupSelector = `#zoomobile-route-${route}`;
   const group = svgRoot?.querySelector(groupSelector);

   if (!group) {
      return;
   }

   const visibleMarkerIds = new Set(markerIds);

   setLayerVisibility(svgRoot, groupSelector, true);
   group.querySelectorAll('circle[id]').forEach((circle) => {
      circle.style.setProperty(
         'display',
         visibleMarkerIds.has(circle.id) ? '' : 'none'
      );
   });
   appendRouteArrows(svgRoot, group, markerSequences);
}
