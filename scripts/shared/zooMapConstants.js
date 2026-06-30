// Keep in sync with api/seed/data/walk_graph.json and images/map/zoo-map.svg.
export const ZOO_MAP_WIDTH_PX = 4096;
export const ZOO_MAP_HEIGHT_PX = 2665;
export const ZOO_MAP_VIEW_BOX = `0 0 ${ZOO_MAP_WIDTH_PX} ${ZOO_MAP_HEIGHT_PX}`;

export const ENTRANCE_WALK_NODE_ID = 'v-0013';

export const ENTRANCE_LANDMARK = Object.freeze({
   nodeId: 'entrance-landmark',
   x: 59.812,
   y: 85.689,
   xPx: 59.812 / 100 * ZOO_MAP_WIDTH_PX,
   yPx: 85.689 / 100 * ZOO_MAP_HEIGHT_PX,
});
