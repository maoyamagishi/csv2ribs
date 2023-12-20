import csv
from pathlib import Path

class csvReader:
   def Reader():
      _fileparent = Path(__file__).resolve().parent
      with open(_fileparent.joinpath("ribsData.csv"),"r") as f:
         reader = csv.reader(f)
         output = []
         for row in reader:
            output.append(row)
         return output

   def FileFormatCertification(arg):
      key = arg[0][0]
      if key == "12345":
         return True
      else:
         return False
