import { VisitDateEarliest } from '../itinerary/visitDateEarliest.js';
import { LoadInlineZooMap } from '../map/loadInlineZooMap.js';
import { MapRuntime } from '../map/mapRuntime.js';
import { TransportationRouteControls } from '../map/transportationRouteControls.js';
import { MapPageBootstrap } from './mapPageBootstrap.js';
import { ExploreUpdates } from '../updates/exploreUpdates.js';

export class MapPage {
   static async initMapPage() {
      const elements = MapPageBootstrap.getMapPageElements();

      if (!MapPageBootstrap.hasRequiredMapPageElements(elements)) return;

      await LoadInlineZooMap.loadInlineZooMap();
      await TransportationRouteControls.initTransportationRouteControls(elements.transportationRoutesEl);

      let explore = null;
      let search = null;
      const updates = ExploreUpdates.createExploreUpdates({
         listEl: elements.exploreUpdatesListEl,
      });

      const runtime = MapRuntime.createMapRuntime(MapPageBootstrap.createRuntimeOptions(elements, {
         getSelectedTypes: () => explore?.getSelectedTypes?.() || [],
         updates,
      }));

      if (!runtime) return;

      const { updater } = runtime;
      const getSearch = () => search;

      explore = MapPageBootstrap.initMapExploreFilter({
         updater,
         getSearch,
         animalSearchResultsEl: elements.animalSearchResultsEl,
      });

      search = MapPageBootstrap.initMapSearch({
         elements,
         explore,
         updater,
      });

      const earliestVisitNoon = await VisitDateEarliest.resolveEarliestSelectableVisitDateNoon();

      MapPageBootstrap.initMapPageControls({
         elements,
         updater,
         getSearch,
         earliestSelectableNoon: earliestVisitNoon,
      });

      MapPageBootstrap.initMapDeepLinkFocus(updater);

      MapPageBootstrap.triggerInitialMapUpdate(elements.mapPreset);
   }
}
