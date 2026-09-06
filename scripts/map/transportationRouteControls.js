import { MapApi } from '../api/mapApi.js';
import { AssetKeyNormalizer } from '../assets/assetKeyNormalizer.js';
import { Strings } from '../strings.js';

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
   return `transportationRoute-${AssetKeyNormalizer.normalize(transportationName)}`;
}

function createTransportationRouteSection(transportation) {
   const section = document.createElement('div');
   section.className = 'transportation-route';
   section.dataset.transportation = transportation.name;

   const title = document.createElement('div');
   title.className = 'transportation-route-title';
   title.textContent = Strings.map.transportationRoute.title(transportation.name);

   const options = document.createElement('div');
   options.className = 'transportation-route-options';

   const groupName = radioGroupName(transportation.name);

   options.append(
      createRouteOption({
         groupName,
         value: 'none',
         label: Strings.map.transportationRoute.none,
         checked: true,
      }),
      createRouteOption({
         groupName,
         value: 'current',
         label: Strings.map.transportationRoute.current,
      }),
      ...transportation.routes.map((route) => createRouteOption({
         groupName,
         value: route,
         label: Strings.map.transportationRoute.route(route),
      })),
   );

   section.append(title, options);
   return section;
}

export class TransportationRouteControls {
   static renderTransportationRouteControls(container, transportations) {
      if (!container) {
         return;
      }

      container.replaceChildren(
         ...transportations.map(createTransportationRouteSection),
      );
   }

   static async initTransportationRouteControls(container) {
      const transportations = await MapApi.getTransportationRoutes();
      TransportationRouteControls.renderTransportationRouteControls(
         container,
         transportations
      );
      return transportations;
   }
}
