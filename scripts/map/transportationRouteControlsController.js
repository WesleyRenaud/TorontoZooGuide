import { MapClient } from '../api/mapClient.js';
import { TransportationRouteControlsBuilder } from './transportationRouteControlsBuilder.js';

export class TransportationRouteControlsController {
   static renderTransportationRouteControls(container, transportations) {
      if (!container) {
         return;
      }

      container.replaceChildren(
         ...transportations.map(TransportationRouteControlsBuilder.createTransportationRouteSection),
      );
   }

   static async initTransportationRouteControls(container) {
      const transportations = await MapClient.getTransportationRoutes();
      TransportationRouteControlsController.renderTransportationRouteControls(
         container,
         transportations
      );
      return transportations;
   }
}
