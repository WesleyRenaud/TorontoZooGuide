class GiftShopOpeningSchedule:
   def __init__(
         self,
         gift_shop,
         start_date,
         end_date,
         monday,
         tuesday,
         wednesday,
         thursday,
         friday,
         saturday,
         sunday,
         holidays_only,
         message ):
      self.gift_shop = gift_shop
      self.start_date = start_date
      self.end_date = end_date
      self.monday = monday
      self.tuesday = tuesday
      self.wednesday = wednesday
      self.thursday = thursday
      self.friday = friday
      self.saturday = saturday
      self.sunday = sunday
      self.holidays_only = holidays_only
      self.message = message
