import dataverk
import pandas as pd
from dataverk_vault import api as vault_api

vault_api.set_secrets_as_envs()


print("tester knada python pod operator")

with open("test.txt", "w") as f:
  f.write("tester å skrive til fil")
  
print("great success writing to file")
