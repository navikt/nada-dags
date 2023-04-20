from kode.annenmodul import callme

def mycallable():
  import time
  from google.cloud import bigquery
  print("hallo fra en annen modul")
  callme()
  #time.sleep(1000)
  print("farvel")
