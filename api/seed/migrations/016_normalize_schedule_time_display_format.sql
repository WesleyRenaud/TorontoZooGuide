-- Normalize 24-hour clock strings to display format (matches format_display_time_value):
--   '14:00' -> '2:00 PM', '09:30' -> '9:30 AM', '13:45:30' -> '1:45:30 PM'
-- Leaves NULL, blank, existing AM/PM values, and unrecognized strings unchanged.

UPDATE AnimalVisibilitySchedule
SET
   DAILY_START_TIME = CASE
      WHEN DAILY_START_TIME IS NULL OR TRIM( DAILY_START_TIME ) = '' THEN DAILY_START_TIME
      WHEN INSTR( UPPER( DAILY_START_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( DAILY_START_TIME ), ' PM' ) > 0 THEN DAILY_START_TIME
      WHEN DAILY_START_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( DAILY_START_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( DAILY_START_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( DAILY_START_TIME, 4, 2 )
            || ':'
            || substr( DAILY_START_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( DAILY_START_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN DAILY_START_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( DAILY_START_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( DAILY_START_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( DAILY_START_TIME, 3, 2 )
            || ':'
            || substr( DAILY_START_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( DAILY_START_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN DAILY_START_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( DAILY_START_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( DAILY_START_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( DAILY_START_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( DAILY_START_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN DAILY_START_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( DAILY_START_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( DAILY_START_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( DAILY_START_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( DAILY_START_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE DAILY_START_TIME
   END,
   DAILY_END_TIME = CASE
      WHEN DAILY_END_TIME IS NULL OR TRIM( DAILY_END_TIME ) = '' THEN DAILY_END_TIME
      WHEN INSTR( UPPER( DAILY_END_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( DAILY_END_TIME ), ' PM' ) > 0 THEN DAILY_END_TIME
      WHEN DAILY_END_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( DAILY_END_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( DAILY_END_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( DAILY_END_TIME, 4, 2 )
            || ':'
            || substr( DAILY_END_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( DAILY_END_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN DAILY_END_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( DAILY_END_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( DAILY_END_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( DAILY_END_TIME, 3, 2 )
            || ':'
            || substr( DAILY_END_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( DAILY_END_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN DAILY_END_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( DAILY_END_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( DAILY_END_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( DAILY_END_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( DAILY_END_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN DAILY_END_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( DAILY_END_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( DAILY_END_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( DAILY_END_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( DAILY_END_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE DAILY_END_TIME
   END;

UPDATE GuardiansTalkSchedule
SET
   MONDAY_TIME = CASE
      WHEN MONDAY_TIME IS NULL OR TRIM( MONDAY_TIME ) = '' THEN MONDAY_TIME
      WHEN INSTR( UPPER( MONDAY_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( MONDAY_TIME ), ' PM' ) > 0 THEN MONDAY_TIME
      WHEN MONDAY_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( MONDAY_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( MONDAY_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( MONDAY_TIME, 4, 2 )
            || ':'
            || substr( MONDAY_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( MONDAY_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN MONDAY_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( MONDAY_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( MONDAY_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( MONDAY_TIME, 3, 2 )
            || ':'
            || substr( MONDAY_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( MONDAY_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN MONDAY_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( MONDAY_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( MONDAY_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( MONDAY_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( MONDAY_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN MONDAY_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( MONDAY_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( MONDAY_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( MONDAY_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( MONDAY_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE MONDAY_TIME
   END,
   TUESDAY_TIME = CASE
      WHEN TUESDAY_TIME IS NULL OR TRIM( TUESDAY_TIME ) = '' THEN TUESDAY_TIME
      WHEN INSTR( UPPER( TUESDAY_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( TUESDAY_TIME ), ' PM' ) > 0 THEN TUESDAY_TIME
      WHEN TUESDAY_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( TUESDAY_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( TUESDAY_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( TUESDAY_TIME, 4, 2 )
            || ':'
            || substr( TUESDAY_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( TUESDAY_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN TUESDAY_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( TUESDAY_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( TUESDAY_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( TUESDAY_TIME, 3, 2 )
            || ':'
            || substr( TUESDAY_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( TUESDAY_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN TUESDAY_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( TUESDAY_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( TUESDAY_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( TUESDAY_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( TUESDAY_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN TUESDAY_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( TUESDAY_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( TUESDAY_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( TUESDAY_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( TUESDAY_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE TUESDAY_TIME
   END,
   WEDNESDAY_TIME = CASE
      WHEN WEDNESDAY_TIME IS NULL OR TRIM( WEDNESDAY_TIME ) = '' THEN WEDNESDAY_TIME
      WHEN INSTR( UPPER( WEDNESDAY_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( WEDNESDAY_TIME ), ' PM' ) > 0 THEN WEDNESDAY_TIME
      WHEN WEDNESDAY_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( WEDNESDAY_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( WEDNESDAY_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( WEDNESDAY_TIME, 4, 2 )
            || ':'
            || substr( WEDNESDAY_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( WEDNESDAY_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN WEDNESDAY_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( WEDNESDAY_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( WEDNESDAY_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( WEDNESDAY_TIME, 3, 2 )
            || ':'
            || substr( WEDNESDAY_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( WEDNESDAY_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN WEDNESDAY_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( WEDNESDAY_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( WEDNESDAY_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( WEDNESDAY_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( WEDNESDAY_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN WEDNESDAY_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( WEDNESDAY_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( WEDNESDAY_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( WEDNESDAY_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( WEDNESDAY_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE WEDNESDAY_TIME
   END,
   THURSDAY_TIME = CASE
      WHEN THURSDAY_TIME IS NULL OR TRIM( THURSDAY_TIME ) = '' THEN THURSDAY_TIME
      WHEN INSTR( UPPER( THURSDAY_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( THURSDAY_TIME ), ' PM' ) > 0 THEN THURSDAY_TIME
      WHEN THURSDAY_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( THURSDAY_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( THURSDAY_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( THURSDAY_TIME, 4, 2 )
            || ':'
            || substr( THURSDAY_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( THURSDAY_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN THURSDAY_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( THURSDAY_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( THURSDAY_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( THURSDAY_TIME, 3, 2 )
            || ':'
            || substr( THURSDAY_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( THURSDAY_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN THURSDAY_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( THURSDAY_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( THURSDAY_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( THURSDAY_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( THURSDAY_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN THURSDAY_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( THURSDAY_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( THURSDAY_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( THURSDAY_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( THURSDAY_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE THURSDAY_TIME
   END,
   FRIDAY_TIME = CASE
      WHEN FRIDAY_TIME IS NULL OR TRIM( FRIDAY_TIME ) = '' THEN FRIDAY_TIME
      WHEN INSTR( UPPER( FRIDAY_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( FRIDAY_TIME ), ' PM' ) > 0 THEN FRIDAY_TIME
      WHEN FRIDAY_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( FRIDAY_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( FRIDAY_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( FRIDAY_TIME, 4, 2 )
            || ':'
            || substr( FRIDAY_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( FRIDAY_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN FRIDAY_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( FRIDAY_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( FRIDAY_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( FRIDAY_TIME, 3, 2 )
            || ':'
            || substr( FRIDAY_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( FRIDAY_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN FRIDAY_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( FRIDAY_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( FRIDAY_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( FRIDAY_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( FRIDAY_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN FRIDAY_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( FRIDAY_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( FRIDAY_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( FRIDAY_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( FRIDAY_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE FRIDAY_TIME
   END,
   SATURDAY_TIME = CASE
      WHEN SATURDAY_TIME IS NULL OR TRIM( SATURDAY_TIME ) = '' THEN SATURDAY_TIME
      WHEN INSTR( UPPER( SATURDAY_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( SATURDAY_TIME ), ' PM' ) > 0 THEN SATURDAY_TIME
      WHEN SATURDAY_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( SATURDAY_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( SATURDAY_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( SATURDAY_TIME, 4, 2 )
            || ':'
            || substr( SATURDAY_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( SATURDAY_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN SATURDAY_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( SATURDAY_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( SATURDAY_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( SATURDAY_TIME, 3, 2 )
            || ':'
            || substr( SATURDAY_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( SATURDAY_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN SATURDAY_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( SATURDAY_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( SATURDAY_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( SATURDAY_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( SATURDAY_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN SATURDAY_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( SATURDAY_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( SATURDAY_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( SATURDAY_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( SATURDAY_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE SATURDAY_TIME
   END,
   SUNDAY_TIME = CASE
      WHEN SUNDAY_TIME IS NULL OR TRIM( SUNDAY_TIME ) = '' THEN SUNDAY_TIME
      WHEN INSTR( UPPER( SUNDAY_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( SUNDAY_TIME ), ' PM' ) > 0 THEN SUNDAY_TIME
      WHEN SUNDAY_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( SUNDAY_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( SUNDAY_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( SUNDAY_TIME, 4, 2 )
            || ':'
            || substr( SUNDAY_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( SUNDAY_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN SUNDAY_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( SUNDAY_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( SUNDAY_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( SUNDAY_TIME, 3, 2 )
            || ':'
            || substr( SUNDAY_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( SUNDAY_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN SUNDAY_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( SUNDAY_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( SUNDAY_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( SUNDAY_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( SUNDAY_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN SUNDAY_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( SUNDAY_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( SUNDAY_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( SUNDAY_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( SUNDAY_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE SUNDAY_TIME
   END;

UPDATE ZooHours
SET
   EARLY_ADMISSION_TIME = CASE
      WHEN EARLY_ADMISSION_TIME IS NULL OR TRIM( EARLY_ADMISSION_TIME ) = '' THEN EARLY_ADMISSION_TIME
      WHEN INSTR( UPPER( EARLY_ADMISSION_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( EARLY_ADMISSION_TIME ), ' PM' ) > 0 THEN EARLY_ADMISSION_TIME
      WHEN EARLY_ADMISSION_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( EARLY_ADMISSION_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( EARLY_ADMISSION_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( EARLY_ADMISSION_TIME, 4, 2 )
            || ':'
            || substr( EARLY_ADMISSION_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( EARLY_ADMISSION_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN EARLY_ADMISSION_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( EARLY_ADMISSION_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( EARLY_ADMISSION_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( EARLY_ADMISSION_TIME, 3, 2 )
            || ':'
            || substr( EARLY_ADMISSION_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( EARLY_ADMISSION_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN EARLY_ADMISSION_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( EARLY_ADMISSION_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( EARLY_ADMISSION_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( EARLY_ADMISSION_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( EARLY_ADMISSION_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN EARLY_ADMISSION_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( EARLY_ADMISSION_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( EARLY_ADMISSION_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( EARLY_ADMISSION_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( EARLY_ADMISSION_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE EARLY_ADMISSION_TIME
   END,
   OPEN_TIME = CASE
      WHEN OPEN_TIME IS NULL OR TRIM( OPEN_TIME ) = '' THEN OPEN_TIME
      WHEN INSTR( UPPER( OPEN_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( OPEN_TIME ), ' PM' ) > 0 THEN OPEN_TIME
      WHEN OPEN_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( OPEN_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( OPEN_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( OPEN_TIME, 4, 2 )
            || ':'
            || substr( OPEN_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( OPEN_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN OPEN_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( OPEN_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( OPEN_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( OPEN_TIME, 3, 2 )
            || ':'
            || substr( OPEN_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( OPEN_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN OPEN_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( OPEN_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( OPEN_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( OPEN_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( OPEN_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN OPEN_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( OPEN_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( OPEN_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( OPEN_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( OPEN_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE OPEN_TIME
   END,
   LAST_ADMISSION_TIME = CASE
      WHEN LAST_ADMISSION_TIME IS NULL OR TRIM( LAST_ADMISSION_TIME ) = '' THEN LAST_ADMISSION_TIME
      WHEN INSTR( UPPER( LAST_ADMISSION_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( LAST_ADMISSION_TIME ), ' PM' ) > 0 THEN LAST_ADMISSION_TIME
      WHEN LAST_ADMISSION_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( LAST_ADMISSION_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( LAST_ADMISSION_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( LAST_ADMISSION_TIME, 4, 2 )
            || ':'
            || substr( LAST_ADMISSION_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( LAST_ADMISSION_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN LAST_ADMISSION_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( LAST_ADMISSION_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( LAST_ADMISSION_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( LAST_ADMISSION_TIME, 3, 2 )
            || ':'
            || substr( LAST_ADMISSION_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( LAST_ADMISSION_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN LAST_ADMISSION_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( LAST_ADMISSION_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( LAST_ADMISSION_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( LAST_ADMISSION_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( LAST_ADMISSION_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN LAST_ADMISSION_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( LAST_ADMISSION_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( LAST_ADMISSION_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( LAST_ADMISSION_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( LAST_ADMISSION_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE LAST_ADMISSION_TIME
   END,
   CLOSE_TIME = CASE
      WHEN CLOSE_TIME IS NULL OR TRIM( CLOSE_TIME ) = '' THEN CLOSE_TIME
      WHEN INSTR( UPPER( CLOSE_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( CLOSE_TIME ), ' PM' ) > 0 THEN CLOSE_TIME
      WHEN CLOSE_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( CLOSE_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( CLOSE_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( CLOSE_TIME, 4, 2 )
            || ':'
            || substr( CLOSE_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( CLOSE_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN CLOSE_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( CLOSE_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( CLOSE_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( CLOSE_TIME, 3, 2 )
            || ':'
            || substr( CLOSE_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( CLOSE_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN CLOSE_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( CLOSE_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( CLOSE_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( CLOSE_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( CLOSE_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN CLOSE_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( CLOSE_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( CLOSE_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( CLOSE_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( CLOSE_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE CLOSE_TIME
   END;

UPDATE ItineraryDate
SET
   ARRIVAL_TIME = CASE
      WHEN ARRIVAL_TIME IS NULL OR TRIM( ARRIVAL_TIME ) = '' THEN ARRIVAL_TIME
      WHEN INSTR( UPPER( ARRIVAL_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( ARRIVAL_TIME ), ' PM' ) > 0 THEN ARRIVAL_TIME
      WHEN ARRIVAL_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( ARRIVAL_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( ARRIVAL_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( ARRIVAL_TIME, 4, 2 )
            || ':'
            || substr( ARRIVAL_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( ARRIVAL_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN ARRIVAL_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( ARRIVAL_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( ARRIVAL_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( ARRIVAL_TIME, 3, 2 )
            || ':'
            || substr( ARRIVAL_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( ARRIVAL_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN ARRIVAL_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( ARRIVAL_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( ARRIVAL_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( ARRIVAL_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( ARRIVAL_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN ARRIVAL_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( ARRIVAL_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( ARRIVAL_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( ARRIVAL_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( ARRIVAL_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE ARRIVAL_TIME
   END,
   DEPARTURE_TIME = CASE
      WHEN DEPARTURE_TIME IS NULL OR TRIM( DEPARTURE_TIME ) = '' THEN DEPARTURE_TIME
      WHEN INSTR( UPPER( DEPARTURE_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( DEPARTURE_TIME ), ' PM' ) > 0 THEN DEPARTURE_TIME
      WHEN DEPARTURE_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( DEPARTURE_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( DEPARTURE_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( DEPARTURE_TIME, 4, 2 )
            || ':'
            || substr( DEPARTURE_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( DEPARTURE_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN DEPARTURE_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( DEPARTURE_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( DEPARTURE_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( DEPARTURE_TIME, 3, 2 )
            || ':'
            || substr( DEPARTURE_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( DEPARTURE_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN DEPARTURE_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( DEPARTURE_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( DEPARTURE_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( DEPARTURE_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( DEPARTURE_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN DEPARTURE_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( DEPARTURE_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( DEPARTURE_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( DEPARTURE_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( DEPARTURE_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE DEPARTURE_TIME
   END;

UPDATE ItineraryAnimal
SET
   START_TIME = CASE
      WHEN START_TIME IS NULL OR TRIM( START_TIME ) = '' THEN START_TIME
      WHEN INSTR( UPPER( START_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( START_TIME ), ' PM' ) > 0 THEN START_TIME
      WHEN START_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 4, 2 )
            || ':'
            || substr( START_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN START_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 3, 2 )
            || ':'
            || substr( START_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN START_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN START_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE START_TIME
   END,
   END_TIME = CASE
      WHEN END_TIME IS NULL OR TRIM( END_TIME ) = '' THEN END_TIME
      WHEN INSTR( UPPER( END_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( END_TIME ), ' PM' ) > 0 THEN END_TIME
      WHEN END_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 4, 2 )
            || ':'
            || substr( END_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN END_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 3, 2 )
            || ':'
            || substr( END_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN END_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN END_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE END_TIME
   END;

UPDATE ItineraryAttraction
SET
   START_TIME = CASE
      WHEN START_TIME IS NULL OR TRIM( START_TIME ) = '' THEN START_TIME
      WHEN INSTR( UPPER( START_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( START_TIME ), ' PM' ) > 0 THEN START_TIME
      WHEN START_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 4, 2 )
            || ':'
            || substr( START_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN START_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 3, 2 )
            || ':'
            || substr( START_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN START_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN START_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE START_TIME
   END,
   END_TIME = CASE
      WHEN END_TIME IS NULL OR TRIM( END_TIME ) = '' THEN END_TIME
      WHEN INSTR( UPPER( END_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( END_TIME ), ' PM' ) > 0 THEN END_TIME
      WHEN END_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 4, 2 )
            || ':'
            || substr( END_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN END_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 3, 2 )
            || ':'
            || substr( END_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN END_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN END_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE END_TIME
   END;

UPDATE ItineraryGuardiansTalk
SET
   START_TIME = CASE
      WHEN START_TIME IS NULL OR TRIM( START_TIME ) = '' THEN START_TIME
      WHEN INSTR( UPPER( START_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( START_TIME ), ' PM' ) > 0 THEN START_TIME
      WHEN START_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 4, 2 )
            || ':'
            || substr( START_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN START_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 3, 2 )
            || ':'
            || substr( START_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN START_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN START_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE START_TIME
   END,
   END_TIME = CASE
      WHEN END_TIME IS NULL OR TRIM( END_TIME ) = '' THEN END_TIME
      WHEN INSTR( UPPER( END_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( END_TIME ), ' PM' ) > 0 THEN END_TIME
      WHEN END_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 4, 2 )
            || ':'
            || substr( END_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN END_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 3, 2 )
            || ':'
            || substr( END_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN END_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN END_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE END_TIME
   END;

UPDATE ItineraryWildEncounter
SET
   START_TIME = CASE
      WHEN START_TIME IS NULL OR TRIM( START_TIME ) = '' THEN START_TIME
      WHEN INSTR( UPPER( START_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( START_TIME ), ' PM' ) > 0 THEN START_TIME
      WHEN START_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 4, 2 )
            || ':'
            || substr( START_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN START_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 3, 2 )
            || ':'
            || substr( START_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN START_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN START_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE START_TIME
   END,
   END_TIME = CASE
      WHEN END_TIME IS NULL OR TRIM( END_TIME ) = '' THEN END_TIME
      WHEN INSTR( UPPER( END_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( END_TIME ), ' PM' ) > 0 THEN END_TIME
      WHEN END_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 4, 2 )
            || ':'
            || substr( END_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN END_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 3, 2 )
            || ':'
            || substr( END_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN END_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN END_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE END_TIME
   END;

UPDATE ItineraryWalkRouteStop
SET
   START_TIME = CASE
      WHEN START_TIME IS NULL OR TRIM( START_TIME ) = '' THEN START_TIME
      WHEN INSTR( UPPER( START_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( START_TIME ), ' PM' ) > 0 THEN START_TIME
      WHEN START_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 4, 2 )
            || ':'
            || substr( START_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN START_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 3, 2 )
            || ':'
            || substr( START_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN START_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN START_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE START_TIME
   END,
   END_TIME = CASE
      WHEN END_TIME IS NULL OR TRIM( END_TIME ) = '' THEN END_TIME
      WHEN INSTR( UPPER( END_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( END_TIME ), ' PM' ) > 0 THEN END_TIME
      WHEN END_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 4, 2 )
            || ':'
            || substr( END_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN END_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 3, 2 )
            || ':'
            || substr( END_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN END_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN END_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE END_TIME
   END;

DROP TABLE IF EXISTS WildEncounterScheduleMigration;

CREATE TABLE WildEncounterScheduleMigration
(  WILD_ENCOUNTER         VARCHAR(64) NOT NULL,
   SCHEDULE_START_DATE    DATE        NOT NULL,
   SCHEDULE_END_DATE      DATE,
   MONDAY                 BOOL        NOT NULL DEFAULT 0,
   TUESDAY                BOOL        NOT NULL DEFAULT 0,
   WEDNESDAY              BOOL        NOT NULL DEFAULT 0,
   THURSDAY               BOOL        NOT NULL DEFAULT 0,
   FRIDAY                 BOOL        NOT NULL DEFAULT 0,
   SATURDAY               BOOL        NOT NULL DEFAULT 0,
   SUNDAY                 BOOL        NOT NULL DEFAULT 0,
   ENCOUNTER_TIME         TEXT        NOT NULL,
   SCHEDULE_MESSAGE       TEXT,
   PRIMARY KEY (WILD_ENCOUNTER, ENCOUNTER_TIME),
   FOREIGN KEY (WILD_ENCOUNTER) REFERENCES WildEncounter(NAME) );

INSERT OR IGNORE INTO WildEncounterScheduleMigration (
   WILD_ENCOUNTER,
   SCHEDULE_START_DATE,
   SCHEDULE_END_DATE,
   MONDAY,
   TUESDAY,
   WEDNESDAY,
   THURSDAY,
   FRIDAY,
   SATURDAY,
   SUNDAY,
   ENCOUNTER_TIME,
   SCHEDULE_MESSAGE
)
SELECT
   WILD_ENCOUNTER,
   SCHEDULE_START_DATE,
   SCHEDULE_END_DATE,
   MONDAY,
   TUESDAY,
   WEDNESDAY,
   THURSDAY,
   FRIDAY,
   SATURDAY,
   SUNDAY,
   CASE
      WHEN ENCOUNTER_TIME IS NULL OR TRIM( ENCOUNTER_TIME ) = '' THEN ENCOUNTER_TIME
      WHEN INSTR( UPPER( ENCOUNTER_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( ENCOUNTER_TIME ), ' PM' ) > 0 THEN ENCOUNTER_TIME
      WHEN ENCOUNTER_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( ENCOUNTER_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( ENCOUNTER_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( ENCOUNTER_TIME, 4, 2 )
            || ':'
            || substr( ENCOUNTER_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( ENCOUNTER_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN ENCOUNTER_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( ENCOUNTER_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( ENCOUNTER_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( ENCOUNTER_TIME, 3, 2 )
            || ':'
            || substr( ENCOUNTER_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( ENCOUNTER_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN ENCOUNTER_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( ENCOUNTER_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( ENCOUNTER_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( ENCOUNTER_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( ENCOUNTER_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN ENCOUNTER_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( ENCOUNTER_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( ENCOUNTER_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( ENCOUNTER_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( ENCOUNTER_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE ENCOUNTER_TIME
   END,
   SCHEDULE_MESSAGE
FROM WildEncounterSchedule;

DROP TABLE WildEncounterSchedule;

ALTER TABLE WildEncounterScheduleMigration RENAME TO WildEncounterSchedule;

DROP TABLE IF EXISTS WildEncounterCancellationMigration;

CREATE TABLE WildEncounterCancellationMigration
(  WILD_ENCOUNTER        VARCHAR(64) NOT NULL,
   CANCELLATION_DATE     DATE        NOT NULL,
   ENCOUNTER_TIME        TEXT        NOT NULL,
   PRIMARY KEY (WILD_ENCOUNTER, CANCELLATION_DATE, ENCOUNTER_TIME),
   FOREIGN KEY (WILD_ENCOUNTER) REFERENCES WildEncounter(NAME) );

INSERT OR IGNORE INTO WildEncounterCancellationMigration (
   WILD_ENCOUNTER,
   CANCELLATION_DATE,
   ENCOUNTER_TIME
)
SELECT
   WILD_ENCOUNTER,
   CANCELLATION_DATE,
   CASE
      WHEN ENCOUNTER_TIME IS NULL OR TRIM( ENCOUNTER_TIME ) = '' THEN ENCOUNTER_TIME
      WHEN INSTR( UPPER( ENCOUNTER_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( ENCOUNTER_TIME ), ' PM' ) > 0 THEN ENCOUNTER_TIME
      WHEN ENCOUNTER_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( ENCOUNTER_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( ENCOUNTER_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( ENCOUNTER_TIME, 4, 2 )
            || ':'
            || substr( ENCOUNTER_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( ENCOUNTER_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN ENCOUNTER_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( ENCOUNTER_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( ENCOUNTER_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( ENCOUNTER_TIME, 3, 2 )
            || ':'
            || substr( ENCOUNTER_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( ENCOUNTER_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN ENCOUNTER_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( ENCOUNTER_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( ENCOUNTER_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( ENCOUNTER_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( ENCOUNTER_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN ENCOUNTER_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( ENCOUNTER_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( ENCOUNTER_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( ENCOUNTER_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( ENCOUNTER_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE ENCOUNTER_TIME
   END
FROM WildEncounterCancellation;

DROP TABLE WildEncounterCancellation;

ALTER TABLE WildEncounterCancellationMigration RENAME TO WildEncounterCancellation;

DROP TABLE IF EXISTS GuardiansTalkCancellationMigration;

CREATE TABLE GuardiansTalkCancellationMigration
(  TALK_NAME             VARCHAR(64) NOT NULL,
   LOCATION              VARCHAR(64) NOT NULL,
   CANCELLATION_DATE     DATE        NOT NULL,
   TALK_TIME             TEXT        NOT NULL,
   PRIMARY KEY (TALK_NAME, LOCATION, CANCELLATION_DATE, TALK_TIME),
   FOREIGN KEY (TALK_NAME, LOCATION) REFERENCES MeetTheGuardiansTalk(NAME, LOCATION) );

INSERT OR IGNORE INTO GuardiansTalkCancellationMigration (
   TALK_NAME,
   LOCATION,
   CANCELLATION_DATE,
   TALK_TIME
)
SELECT
   TALK_NAME,
   LOCATION,
   CANCELLATION_DATE,
   CASE
      WHEN TALK_TIME IS NULL OR TRIM( TALK_TIME ) = '' THEN TALK_TIME
      WHEN INSTR( UPPER( TALK_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( TALK_TIME ), ' PM' ) > 0 THEN TALK_TIME
      WHEN TALK_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( TALK_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( TALK_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( TALK_TIME, 4, 2 )
            || ':'
            || substr( TALK_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( TALK_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN TALK_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( TALK_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( TALK_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( TALK_TIME, 3, 2 )
            || ':'
            || substr( TALK_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( TALK_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN TALK_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( TALK_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( TALK_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( TALK_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( TALK_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN TALK_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( TALK_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( TALK_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( TALK_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( TALK_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE TALK_TIME
   END
FROM GuardiansTalkCancellation;

DROP TABLE GuardiansTalkCancellation;

ALTER TABLE GuardiansTalkCancellationMigration RENAME TO GuardiansTalkCancellation;

DROP TABLE IF EXISTS ItineraryEventMigration;

CREATE TABLE ItineraryEventMigration
(  EVENT_TYPE           TEXT        NOT NULL,
   START_TIME           TEXT        NOT NULL,
   END_TIME             TEXT,
   PRIMARY KEY ( EVENT_TYPE, START_TIME ) );

INSERT OR IGNORE INTO ItineraryEventMigration (
   EVENT_TYPE,
   START_TIME,
   END_TIME
)
SELECT
   EVENT_TYPE,
   CASE
      WHEN START_TIME IS NULL OR TRIM( START_TIME ) = '' THEN START_TIME
      WHEN INSTR( UPPER( START_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( START_TIME ), ' PM' ) > 0 THEN START_TIME
      WHEN START_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 4, 2 )
            || ':'
            || substr( START_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN START_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 3, 2 )
            || ':'
            || substr( START_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN START_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN START_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( START_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( START_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE START_TIME
   END,
   CASE
      WHEN END_TIME IS NULL OR TRIM( END_TIME ) = '' THEN END_TIME
      WHEN INSTR( UPPER( END_TIME ), ' AM' ) > 0
         OR INSTR( UPPER( END_TIME ), ' PM' ) > 0 THEN END_TIME
      WHEN END_TIME GLOB '[0-9][0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 4, 2 )
            || ':'
            || substr( END_TIME, 7, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN END_TIME GLOB '[0-9]:[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 3, 2 )
            || ':'
            || substr( END_TIME, 5, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN END_TIME GLOB '[0-9][0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 4, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 2 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      WHEN END_TIME GLOB '[0-9]:[0-9][0-9]'
         THEN LTRIM(
            CASE
               WHEN ( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 ) = 0
                  THEN '12'
               ELSE CAST( CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) % 12 AS TEXT )
            END
            || ':'
            || substr( END_TIME, 3, 2 )
            || CASE
                  WHEN CAST( substr( END_TIME, 1, 1 ) AS INTEGER ) < 12
                     THEN ' AM'
                  ELSE ' PM'
               END,
            '0' )
      ELSE END_TIME
   END
FROM ItineraryEvent;

DROP TABLE ItineraryEvent;

ALTER TABLE ItineraryEventMigration RENAME TO ItineraryEvent;
