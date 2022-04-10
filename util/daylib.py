from datetime import datetime as dt
from datetime import  timedelta, timezone
import pytz
import os

# D: Date
# None: datetime
class daylib():
    # Constant obj
    utc_tz = pytz.timezone('UTC')
    
    @classmethod
    def currentTime(cls, offset=None):
        dt_offset = dt.now().astimezone(timezone(timedelta(hours=offset)))
        return dt_offset
    
    @classmethod
    def valid_intD(cls, int_date, allow_future=True):
        assert type(int_date) == int, f'int_date must be int. Not:{type(int_date)}'
        if (int_date < 20000101)or(int_date>21001231):
            raise Exception("int_date must be 8-digits and following realworld")
        
        if not allow_future :
            if (int_date >= cls.dt_to_intD(cls.currentTime())):
                raise Exception("Future date.")
            
        return True

    @classmethod
    def intD_to_dt(cls, int_date):
        cls.valid_intD(int_date)
        return dt.strptime(str(int_date),'%Y%m%d')

    @classmethod
    def intD_to_strYMD(cls, int_date):
        dt_obj=cls.intD_to_dt(int_date)
        str_date = cls.dt_to_strYMD(dt_obj)
        return str_date
    
    @classmethod
    def intD_to_strD(cls, int_date):
        cls.valid_intD(int_date)
        return str(int_date)

    @classmethod
    def dt_to_intD(cls, dt_obj):
        return int(dt_obj.strftime('%Y%m%d'))

    @classmethod
    def dt_to_strYMDHM(cls, dt_obj):
        return dt_obj.strftime('%Y%m%d%H%M')

    @classmethod
    def dt_to_strYMDHMSF(cls, dt_obj):
        return dt_obj.strftime('%Y%m%d%H%M%S%f')
    
    @classmethod
    def dt_to_strYMDHMSFformat(cls, dt_obj):
        return dt_obj.strftime('%Y-%m-%d %H:%M:%S.%f')
    
    @classmethod
    def strYMDHMSF_to_dt(cls, str_dt):
        return dt.strptime(str_dt, '%Y%m%d%H%M%S%f')
    
    @classmethod
    def dt_to_strYMD(cls, dt_obj):
        return dt_obj.strftime('%Y-%m-%d')

    @classmethod
    def str_utc_to_dt_offset(cls, str_utc, local_tz_str=None,is_T=True,is_ms=True, is_Z=True):
        format = '%Y-%m-%d'

        T =  'T' if  is_T else ' '
        format = format + T
        if is_ms:
            format = format +'%H:%M:%S.%f'
        else:
            format = format +'%H:%M:%S'
        # format += '.%z'
        format +=  'Z' if  is_Z else ''
        
        local_tz_str = "Asia/Tokyo" if local_tz_str is None else local_tz_str
        local_tz = pytz.timezone(local_tz_str) 

        
        dt_utc = dt.strptime(str_utc, format) #naive
        dt_utc_tz = cls.utc_tz.localize(dt_utc) #aware
        dt_local_tz=local_tz.normalize(dt_utc_tz)#localize
        return dt_local_tz


    @classmethod
    def add_day(cls, int_date, offset):
        # No checl : OK
        dt_obj = cls.intD_to_dt(int_date)
        dt_obj = dt_obj+ timedelta(days=offset)
        return cls.dt_to_intD(dt_obj)

    @classmethod
    def get_between_date(cls, since_int_date, until_int_date) :
        _ = cls.valid_intD(since_int_date)    
        _ = cls.valid_intD(until_int_date)
        _int_date = since_int_date
        dates = []
        while True:
            if  _int_date > until_int_date:
                break
            dates.append(_int_date)
            _int_date = cls.add_day(_int_date,1)
        return dates

