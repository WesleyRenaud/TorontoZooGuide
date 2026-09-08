import { GroupConsecutiveTransportationLegSequencesHelper } from './groupConsecutiveTransportationLegSequencesHelper.js';

/**
 * Split timed transportation legs into onboard/offboard ride sequences.
 * A new sequence starts when stations are discontinuous or when leg times
 * are not contiguous (guest got off between rides).
 */
export class GroupConsecutiveTransportationLegGrouper {
   static groupConsecutiveTransportationLegSequences(legs = []) {
      const sequences = [];
      let currentSequence = [];

      GroupConsecutiveTransportationLegSequencesHelper.normalizeLegs(legs).forEach((leg) => {
         if (currentSequence.length > 0) {
            const previousLeg = currentSequence[currentSequence.length - 1];
            const stationGap = previousLeg.to_station !== leg.from_station;
            const timeGap = previousLeg.end_time !== leg.start_time;

            if (stationGap || timeGap) {
               sequences.push(currentSequence);
               currentSequence = [];
            }
         }

         currentSequence.push(leg);
      });

      if (currentSequence.length > 0) {
         sequences.push(currentSequence);
      }

      return sequences;
   }
}
