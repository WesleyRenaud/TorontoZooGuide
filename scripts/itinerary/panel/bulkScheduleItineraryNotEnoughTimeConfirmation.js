export const BULK_SCHEDULE_ITINERARY_NOT_ENOUGH_TIME_ISSUE = (
   'bulkScheduleItineraryNotEnoughTime'
);

export function hasBulkScheduleItineraryNotEnoughTimeIssue(issues = []) {
   return issues.some(
      (issue) => issue?.type === BULK_SCHEDULE_ITINERARY_NOT_ENOUGH_TIME_ISSUE
   );
}
