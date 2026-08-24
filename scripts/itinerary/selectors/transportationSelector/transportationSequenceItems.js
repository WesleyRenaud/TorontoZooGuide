import { groupConsecutiveTransportationLegSequences } from './groupConsecutiveTransportationLegSequences.js';
import { hasItineraryScheduleTimes } from '../../panel/rowActionProps.js';
export function buildTransportationSequenceItems(transportation) {
   const sequences = groupConsecutiveTransportationLegSequences(
      transportation?.legs
   );

   if (sequences.length === 0) {
      return hasItineraryScheduleTimes(transportation)
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

export function expandTransportationListItems(
   transportations = [],
   { splitSequences = false } = {}
) {
   if (!splitSequences) {
      return transportations;
   }

   return transportations.flatMap((transportation) => {
      const sequences = buildTransportationSequenceItems(transportation);

      return sequences.length > 0 ? sequences : [transportation];
   });
}
