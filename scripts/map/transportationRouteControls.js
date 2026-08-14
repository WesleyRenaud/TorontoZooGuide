import { getTransportationRoutes } from '../api/mapApi.js';
import { normalizeAssetKey } from '../assets/normalizeAssetKey.js';
import { APP_STRINGS } from '../strings.js';

const ZOOMOBILE_TRANSPORTATION = 'Zoomobile';

function createRouteOption({
   groupName,
   value,
   label,
   checked = false,
}) {
   const option = document.createElement('label');
   option.className = 'transportation-route-option';

   const input = document.createElement('input');
   input.type = 'radio';
   input.name = groupName;
   input.value = value;
   input.checked = checked;

   const text = document.createElement('span');
   text.textContent = label;

   option.append(input, text);
   return option;
}

function radioGroupName(transportationName) {
   if (transportationName === ZOOMOBILE_TRANSPORTATION) {
      return 'zoomobileRoute';
   }

   return `transportationRoute-${normalizeAssetKey(transportationName)}`;
}

function createTransportationRouteSection(transportation) {
   const section = document.createElement('div');
   section.className = 'transportation-route';
   section.dataset.transportation = transportation.name;

   const title = document.createElement('div');
   title.className = 'transportation-route-title';
   title.textContent = APP_STRINGS.map.transportationRoute.title(transportation.name);

   const options = document.createElement('div');
   options.className = 'transportation-route-options';

   const groupName = radioGroupName(transportation.name);

   options.append(
      createRouteOption({
         groupName,
         value: 'none',
         label: APP_STRINGS.map.transportationRoute.none,
         checked: true,
      }),
      createRouteOption({
         groupName,
         value: 'current',
         label: APP_STRINGS.map.transportationRoute.current,
      }),
      ...transportation.routes.map((route) => createRouteOption({
         groupName,
         value: route,
         label: APP_STRINGS.map.transportationRoute.route(route),
      })),
   );

   section.append(title, options);
   return section;
}

export function renderTransportationRouteControls(container, transportations) {
   if (!container) {
      return;
   }

   container.replaceChildren(
      ...transportations.map(createTransportationRouteSection),
   );
}

export async function initTransportationRouteControls(container) {
   const transportations = await getTransportationRoutes();
   renderTransportationRouteControls(container, transportations);
   return transportations;
}
