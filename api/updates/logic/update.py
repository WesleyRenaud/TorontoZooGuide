from ... import zoo


def filter_updates_started_on_or_before( updates, as_of_date ):
   return [
      update
      for update in updates
      if zoo.ZooUtil.is_date_on_or_after( as_of_date, update.start_date )
   ]
