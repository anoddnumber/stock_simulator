from googlefinance import getQuotes
import json

print json.dumps(getQuotes(['MSFT']), indent=2)
