export const BULK_SCHEDULE_ANIMALS_NOT_ENOUGH_TIME_ISSUE = (
   'bulkScheduleAnimalsNotEnoughTime'
);

export function hasBulkScheduleAnimalsNotEnoughTimeIssue(issues = []) {
   return issues.some(
      (issue) => issue?.type === BULK_SCHEDULE_ANIMALS_NOT_ENOUGH_TIME_ISSUE
   );
}
