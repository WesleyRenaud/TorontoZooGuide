import { VisitDateResolver } from '../itinerary/visitDateResolver.js';
import { LikelihoodColors } from '../likelihood/likelihoodColors.js';
import { LoadInlineZooMapLoader } from '../map/loadInlineZooMapLoader.js';
import { MapFactory } from '../map/mapFactory.js';
import { TransportationRouteControlsController } from '../map/transportationRouteControlsController.js';
import { MapPageBootstrap } from './mapPageBootstrap.js';
import { ExploreFragment } from '../updates/exploreFragment.js';

export class MapBootstrap {
   static paintPinKey() {
      const bar = document.querySelector('.map-pin-key-bar');

      if (!bar) return;

      bar.style.backgroundImage = LikelihoodColors.toGradient();
   }

   static async initMapPage() {
      MapBootstrap.paintPinKey();

      const elements = MapPageBootstrap.getMapPageElements();

      if (!MapPageBootstrap.hasRequiredMapPageElements(elements)) return;

      const svgReady = LoadInlineZooMapLoader.loadInlineZooMap();
      const transportationReady = TransportationRouteControlsController.initTransportationRouteControls(
         elements.transportationRoutesEl,
      );
      const earliestVisitNoonReady = VisitDateResolver.resolveEarliestSelectableVisitDateNoon();

      await Promise.all([
         svgReady,
         transportationReady,
         earliestVisitNoonReady,
      ]);

      const earliestVisitNoon = await earliestVisitNoonReady;

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
