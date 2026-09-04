export class BulkScheduleItineraryNotEnoughTimeConfirmation {
   static BULK_SCHEDULE_ITINERARY_NOT_ENOUGH_TIME_ISSUE = (
      'bulkScheduleItineraryNotEnoughTime'
   );

   static hasBulkScheduleItineraryNotEnoughTimeIssue(issues = []) {
      return issues.some(
         (issue) => (
            issue?.type
            === BulkScheduleItineraryNotEnoughTimeConfirmation
               .BULK_SCHEDULE_ITINERARY_NOT_ENOUGH_TIME_ISSUE
         )
      );
   }
}
