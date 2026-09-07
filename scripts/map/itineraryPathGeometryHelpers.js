export class ItineraryPathGeometryHelpers {
   static legsShareJoinNode(previousLeg, currentLeg) {
      return (
         previousLeg.nodeIds[previousLeg.nodeIds.length - 1]
         === currentLeg.nodeIds[0]
      );
   }
}
