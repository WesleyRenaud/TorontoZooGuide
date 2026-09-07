import { MapApi } from '../api/mapApi.js';
import { TransportationRouteControlsBuilder } from './transportationRouteControlsBuilder.js';

export class TransportationRouteControls {
   static renderTransportationRouteControls(container, transportations) {
      if (!container) {
         return;
      }

      container.replaceChildren(
         ...transportations.map(TransportationRouteControlsBuilder.createTransportationRouteSection),
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
