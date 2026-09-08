import { VisitDateResolver } from '../itinerary/visitDateResolver.js';
import { LoadInlineZooMapLoader } from '../map/loadInlineZooMapLoader.js';
import { MapFactory } from '../map/mapFactory.js';
import { TransportationRouteControlsController } from '../map/transportationRouteControlsController.js';
import { MapPageBootstrap } from './mapPageBootstrap.js';
import { ExploreFragment } from '../updates/exploreFragment.js';

export class MapBootstrap {
   static async initMapPage() {
      const elements = MapPageBootstrap.getMapPageElements();

      if (!MapPageBootstrap.hasRequiredMapPageElements(elements)) return;

      await LoadInlineZooMapLoader.loadInlineZooMap();
      await TransportationRouteControlsController.initTransportationRouteControls(elements.transportationRoutesEl);

      let explore = null;
      let search = null;
      const updates = ExploreFragment.createExploreUpdates({
         listEl: elements.exploreUpdatesListEl,
      });

      const runtime = MapFactory.createMapRuntime(MapPageBootstrap.createRuntimeOptions(elements, {
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

      const earliestVisitNoon = await VisitDateResolver.resolveEarliestSelectableVisitDateNoon();

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
