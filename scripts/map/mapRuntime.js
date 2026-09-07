import { AppConfig } from '../config/appConfig.js';
import { MapDataSourceFactory } from './mapDataSourceFactory.js';
import { MapRuntimeFactory } from './mapRuntimeFactory.js';
import { MapUpdater } from './mapUpdater.js';
import { HoverTooltip } from '../markers/hoverTooltip.js';
import { Markers } from '../markers/markers.js';
import { SpeciesOverlay } from '../overlays/speciesOverlay.js';
import { Panzoom } from './panzoom.js';
import { Store } from './store.js';

export class MapRuntime {
   static createMapRuntime({
   mapInner,
   tooltipEl,
   hoverTooltipEl,
   showMapLabelsCheckbox = null,
   enableCoordinateEditing = false,
   getIncludeOffDisplay = () => false,
   getIncludeClosedRestaurants = () => false,
   getIncludeClosedRestrooms = () => false,
   getIncludeClosedGiftShops = () => false,
   getIncludeClosedAttractions = () => false,
   getTransportationRoute = () => 'none',
   getSelectedTypes = () => [],
   onDateContextChange = null,
} = {}) {
      const viewportEl = mapInner?.parentElement;

      if (!MapRuntimeFactory.hasRequiredRuntimeElements({ mapInner, tooltipEl, viewportEl })) {
         return null;
      }

      const panzoom = Panzoom.createPanzoom(mapInner, { contain: AppConfig.DEFAULT_MAP_CONTAIN });
      const store = Store.createMapStore();
      const sources = MapDataSourceFactory.createDataSources(store);
      const hover = HoverTooltip.createHoverTooltip(hoverTooltipEl);
      const speciesOverlay = SpeciesOverlay.initSpeciesOverlay();

      const tooltip = MapRuntimeFactory.createMapTooltip({
         tooltipEl,
         speciesOverlay,
      });

      MapRuntimeFactory.initMapLabels(showMapLabelsCheckbox);

      const markers = Markers.createMarkerLayer({
         mapInner,
         tooltip,
         hover,
         enableCoordinateEditing,
      });

      const focus = MapRuntimeFactory.createMapFocus({
         panzoom,
         markers,
         tooltip,
         viewportEl,
      });

      const updater = MapUpdater.createMapUpdater({
         store,
         sources,
         markers,
         focus,
         getIncludeOffDisplay,
         getIncludeClosedRestaurants,
         getIncludeClosedRestrooms,
         getIncludeClosedGiftShops,
         getIncludeClosedAttractions,
         getTransportationRoute,
         getSelectedTypes,
         onDateContextChange,
      });

      return {
         panzoom,
         store,
         sources,
         hover,
         tooltip,
         markers,
         focus,
         updater,
         repositionTooltips: MapRuntimeFactory.createTooltipRepositioner({
            tooltip,
            hover,
         }),
      };
   }
}
