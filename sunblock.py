import urllib.request
import json
from  datetime import timedelta,date,datetime
from  time import sleep
import RPi.GPIO as GPIO
import logging
import logging.handlers
from logging.handlers import SysLogHandler


STOP_TLV_PIN =  14  # pin 8:  4th pin from the right on the outside next to ground on pin 6.  

def getUrl(sdate) :
   sitebase="https://mijn.easyenergy.com/nl/api/tariff/getapxtariffs"
   parm_start="startTimestamp="+str(sdate)+"T00:00:00.000Z"
   parm_end="endTimestamp="+str(sdate+timedelta(days=1))+"T00:00:00.000Z"
   return sitebase+"?"+parm_start+"&"+parm_end

def GetInfo(sdate) :
   with urllib.request.urlopen(getUrl(sdate)) as response:
     return json.loads(response.read())

def SleepUntilNextHour() :
   n=datetime.now()
   sleeptime=3601-n.minute*60-n.second
   logger.info("sunblock [info] sleeping for "+str(sleeptime)+" seconds")
   sleep(sleeptime)

def SetGpio(state) :
    if (state) :
       GPIO.output(STOP_TLV_PIN,GPIO.HIGH)
       logger.info("sunblock [info] Negative price: Block")
    else :
       GPIO.output(STOP_TLV_PIN,GPIO.LOW)
       logger.info("sunblock [info] Positive price:  Pass")

def UpdateTable(pr) :
   i=len(pr)-1
   while i >=0  and  datetime.strptime(pr[i]["Timestamp"],'%Y-%m-%dT%H:%M:%S+00:00') > datetime.utcnow():
     i=i-1
   pr = pr[slice(i,len(pr),1)]
   if len(pr) < 24 and datetime.now().strftime("%H") > '15' :
       pr=pr+GetInfo(date.today()+timedelta(days=1))
   logger.info("sunblock [info] Time = "+pr[0]["Timestamp"]+" (UTC) Tariff = "+str(pr[0]["TariffReturn"])+" data for "+str(len(pr))+" hour")
   return pr

if __name__ == "__main__":
   logger = logging.getLogger('sunblock')
   logger.setLevel(logging.INFO)
   handler = logging.handlers.SysLogHandler(facility=SysLogHandler.LOG_DAEMON, address='/dev/log')
   logger.addHandler(handler)
   logger.info("sunblock [info] starting service.")
   GPIO.setmode(GPIO.BCM)
   GPIO.setwarnings(False)
   GPIO.setup(STOP_TLV_PIN,GPIO.OUT)
   tb=GetInfo(date.today())
   while True:
       tb=UpdateTable(tb)
       SetGpio(tb[0]["TariffReturn"] <0)
       SleepUntilNextHour()

