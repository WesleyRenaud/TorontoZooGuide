// Keep in sync with api/seed/data/walk_graph.json and images/map/zoo-map.svg.
export class ZooMapConstants {
   static ZOO_MAP_WIDTH_PX = 4096;
   static ZOO_MAP_HEIGHT_PX = 2665;
   static ZOO_MAP_VIEW_BOX = `0 0 ${this.ZOO_MAP_WIDTH_PX} ${this.ZOO_MAP_HEIGHT_PX}`;

   static ENTRANCE_WALK_NODE_ID = 'v-0001';
}
