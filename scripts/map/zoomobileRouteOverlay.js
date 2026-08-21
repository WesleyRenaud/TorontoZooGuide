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

export function hideZoomobileRouteLayers() {
   const svgRoot = getSvgRoot();

   clearRouteMarkerFilters(svgRoot);
   setLayerVisibility(svgRoot, '#zoomobile-route-summer', false);
   setLayerVisibility(svgRoot, '#zoomobile-route-winter', false);
}

export function showZoomobileRouteLayer(route) {
   const svgRoot = getSvgRoot();

   hideZoomobileRouteLayers();

   if (!route) {
      return;
   }

   setLayerVisibility(svgRoot, `#zoomobile-route-${route}`, true);
}

export function showZoomobileRouteMarkers(route, markerIds) {
   const svgRoot = getSvgRoot();

   hideZoomobileRouteLayers();

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
}
