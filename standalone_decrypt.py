import os
import logging
from pysqlcipher3 import dbapi2 as sqlite
logger = logging.getLogger("wechat")
output = "decrypted.db"
conn = sqlite.connect("EnMicroMsg.db")
c = conn.cursor()
key = ""
#fill the key
c.execute("PRAGMA key = '" + key + "';")
# https://github.com/sqlcipher/sqlcipher/commit/e4b66d6cc8a2b7547a32ff2c3ac52f148eba3516
c.execute("PRAGMA cipher_compatibility = 1;")
try:
	c.execute("ATTACH DATABASE '" + output + "' AS db KEY '';")
except Exception as e:
	logger.error(f"Decryption failed: '{e}'")
	os.unlink(output)
	raise
logger.info(f"Decryption succeeded! Writing database to {output} ...")
c.execute("SELECT sqlcipher_export('db');" )
c.execute("DETACH DATABASE db;" )
c.close()