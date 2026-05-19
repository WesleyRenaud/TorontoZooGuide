from ... import zoo


def build_zoo_hours( zoo_hours_record ):
   return zoo.ZooHours(
      date=zoo_hours_record.operating_date,
      early_admission_time=zoo_hours_record.early_admission_time,
      open_time=zoo_hours_record.open_time,
      last_admission_time=zoo_hours_record.last_admission_time,
      close_time=zoo_hours_record.close_time )
