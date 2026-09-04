import { GroupConsecutiveTransportationLegSequences } from './groupConsecutiveTransportationLegSequences.js';
import { RowActionProps } from '../../panel/rowActionProps.js';

export class TransportationSequenceItems {
   static buildTransportationSequenceItems(transportation) {
      const sequences = GroupConsecutiveTransportationLegSequences.groupConsecutiveTransportationLegSequences(
         transportation?.legs
      );

      if (sequences.length === 0) {
         return RowActionProps.hasItineraryScheduleTimes(transportation)
            ? [transportation]
            : [];
      }

      return sequences.map((sequence) => ({
         ...transportation,
         start_time: sequence[0].start_time,
         end_time: sequence[sequence.length - 1].end_time,
         legs: sequence,
         // Sequence-local stations come from these legs, not parent roles.
         stations: [],
      }));
   }

   static expandTransportationListItems(
      transportations = [],
      { splitSequences = false } = {}
   ) {
      if (!splitSequences) {
         return transportations;
      }

      return transportations.flatMap((transportation) => {
         const sequences = TransportationSequenceItems.buildTransportationSequenceItems(transportation);

         return sequences.length > 0 ? sequences : [transportation];
      });
   }
}
