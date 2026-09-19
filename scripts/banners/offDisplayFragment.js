import { ItineraryTransportationAnimal } from '../itinerary/itineraryTransportationAnimal.js';
import { MessageFragment } from './messageFragment.js';
import { TransportationName } from '../shared/enums/transportationName.js';
import { Strings } from '../strings.js';

export class OffDisplayFragment {
   static createOffDisplayBanner() {
      return MessageFragment.createMessageBanner({
         getMessages: animal => {
            const messages = [];

            if (animal.off_display_message) {
               messages.push(animal.off_display_message);
            }

            if (animal.limited_viewing_message) {
               messages.push(animal.limited_viewing_message);
            }

            if (animal.viewing_alert_messages?.length) {
               messages.push(animal.viewing_alert_messages.join('\n\n'));
            }

            if (ItineraryTransportationAnimal.isAddedByTransportation(animal)) {
               messages.push(
                  Strings.itinerary.map.plannedViaTransportation(animal.transportation)
               );
            } else if (animal.is_zoomobile_only) {
               messages.push(
                  Strings.map.visibleViaTransportation(TransportationName.ZOOMOBILE)
               );
            }

            return [...new Set(messages)];
         },
      });
   }
}
